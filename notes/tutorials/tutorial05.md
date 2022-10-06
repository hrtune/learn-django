# Automated testing

**Why you need to create tests**

* Tests will save you time
* Tests don’t just identify problems, they prevent them
* Tests make your code more attractive
* Tests help teams work together

> Just create and apply tests


## Writing our first test

* Our `Question.was_published_recently()` returns True even if the `pub_date`
    is in the future. 

** Create a test **
`polls/tests.py`
```python
# ...
class QuestionModelTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)
#...
```
* `datetime.timedelta()` is an object represents a duration of time.
    * cf. https://docs.python.org/3/library/datetime.html?highlight=datetime#timedelta-objects
* The function name means "test: was_published_recently() with a future
    question"
* Each test method might call `TestCase.assertIs()`
    * `assertIs(a, b)` checks if `a is b`
    * cf. https://docs.python.org/3/library/unittest.html#unittest.TestCase.debug

## Running tests

Test for the polls
```sh
$ python manage.py test polls
```

## Fix the bug

In `polls/models.py`,
```python
def was_published_recently(self):
    now = timezone.now()
    return now - datetime.timedelta(days=1) <= self.pub_date <= now
```
* 'chaining comparison operators' in return statement
    * `a <= b <= c` iff `a <= b and b <= c` except that b is evaluated once in
        the former.

## More comprehensive tests

`polls/tests.py`
```python
def test_was_published_recently_with_old_question(self):
    """
    was_published_recently() returns False for questions whose pub_date
    is older than 1 day.
    """
    time = timezone.now() - datetime.timedelta(days=1, seconds=1)
    old_question = Question(pub_date=time)
    self.assertIs(old_question.was_published_recently(), False)

def test_was_published_recently_with_recent_question(self):
    """
    was_published_recently() returns True for questions whose pub_date
    is within the last day.
    """
    time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
    recent_question = Question(pub_date=time)
    self.assertIs(recent_question.was_published_recently(), True)
```

## Test a view

** Django test client **

Django provides a test Client to simulate a user interacting with the code at the view level.
We can use it in tests.py or even in the shell.

```sh
$ python manage.py shell
```
```python
from django.test.utils import setup_test_environment
setup_test_environment()
```
* setup_test_environment() installs a template renderer which will allow us to examine some additional attributes on responses such as response.context that otherwise wouldn’t be available.

```python
from django.test import Client
# create an instance of the client for our use
client = Client()
```

```python
# get a response from '/'
response = client.get('/')
response.status_code # this should return 404

from django.urls import reverse
response = client.get(reverse('polls:index'))
response.status_code # this will be 200 (which is OK)
response.content # http content
response.context['latest_question_list']
```

* cf. https://docs.djangoproject.com/en/4.1/topics/testing/tools/
* `Client.get(path)` returns Response object
    * cf. https://docs.djangoproject.com/en/4.1/topics/testing/tools/#testing-responses
    * `Response.context` is a context object which is used to render.

## Improve polls.views

In the IndexView class:
```python
def get_queryset(self):
    """
    Return the last five published questions (not including those set to be
    published in the future).
    """
    return Question.objects.filter(
        pub_date__lte=timezone.now()
    ).order_by('-pub_date')[:5]
```

* The weird double underscores and the following something are called "Field
    lookups"
    * Syntax : `field__lookuptype=value`
    * cf. https://docs.djangoproject.com/en/4.1/topics/db/queries/#field-lookups

## Test with the new view

`polls/tests.py`
```python
def create_question(question_text, days):
    """
    Create a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """
        If no questions exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        """
        Questions with a pub_date in the past are displayed on the
        index page.
        """
        question = create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question],
        )

    def test_future_question(self):
        """
        Questions with a pub_date in the future aren't displayed on
        the index page.
        """
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_question_and_past_question(self):
        """
        Even if both past and future questions exist, only past questions
        are displayed.
        """
        question = create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question],
        )

    def test_two_past_questions(self):
        """
        The questions index page may display multiple questions.
        """
        question1 = create_question(question_text="Past question 1.", days=-30)
        question2 = create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question2, question1],
        )
```

* `SimpleTestCase.assertContains(response, text)` checks if the text appears in
    its content.
* `TransactionTestCase.assertQuerysetEqual(qs, values)` checks if the queryset
    is equal to values, which is a set as a python iterable.

## Test the DetailView

```python
class DetailView(generic.DetailView):
    ...
    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())
```

```python
class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        """
        The detail view of a question with a pub_date in the future
        returns a 404 not found.
        """
        future_question = create_question(question_text='Future question.', days=5)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
        The detail view of a question with a pub_date in the past
        displays the question's text.
        """
        past_question = create_question(question_text='Past Question.', days=-5)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)
```


