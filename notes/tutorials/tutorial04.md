# Forms

https://docs.djangoproject.com/en/4.1/intro/tutorial04/

** Write a minimal form **
A template `polls/detail.html`
```html
<form action="{% url 'polls:vote' question.id %}" method="post">
{% csrf_token %}
<fieldset>
    <legend><h1>{{ question.question_text }}</h1></legend>
    {% if error_message %}<p><strong>{{ error_message }}</strong></p>{% endif %}
    {% for choice in question.choice_set.all %}
        <input type="radio" name="choice" id="choice{{ forloop.counter }}" value="{{ choice.id }}">
        <label for="choice{{ forloop.counter }}">{{ choice.choice_text }}</label><br>
    {% endfor %}
</fieldset>
<input type="submit" value="Vote">
</form>
```

* The request method must be 'post'.
* `<fieldset>` groups an html form
    * `<legend>` is a caption for the fieldset
* `{% csrf_token %}` protects the form against the CSRF
* `forloop.counter` indicates how many times the for tag has gone through its loop
* This form creates a POST message; name:value pairs of a dictionary.

===

** Add a url for post requests **
`polls/urls.py`
```python
    #...
    path('<int:question_id>/vote/', views.vote, name='vote'),
    #...
```

===

** Implement the vote **
`polls/views.py`
```python
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
```
* `request.POST` is a dictionary like object from the POST request.
    * Since both `pk=1` and `pk='1'` are acceptable, `pk=request.POST[...]` is
      okay.
* Abide by the rule "POST-REDIRECT-GET-Refresh" rule for a user to avoid the
    "double posts".
* `HttpResponseRedirect()` takes a fully qualified URL to which django
    redirects.
    * c.f. https://docs.djangoproject.com/en/4.1/ref/request-response/#django.http.HttpResponseRedirect
* `reverse()` converts 'URL pattern name' to a url string defined in urls.
    * `viewname` : URL pattern name as a string
    * `args` : arguments for the url to resolve

===

** Result view **
`polls/templates/polls/results.html`
```html
<h1>{{ question.question_text }}</h1>

<ul>
{% for choice in question.choice_set.all %}
    <li>{{ choice.choice_text }} -- {{ choice.votes }} vote{{ choice.votes|pluralize }}</li>
{% endfor %}
</ul>

<a href="{% url 'polls:detail' question.id %}">Vote again?</a>
```
* The weird keyword with a pipe `|pluralize` is called "built-in filter"
    * c.f. https://docs.djangoproject.com/en/4.1/ref/templates/builtins/#built-in-filter-reference
    * `variable|pluralize` returns 's' if the value is not 1, '1', or its length is not 1.

===

** Class based views **

```python
class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'
```
* There are two generic views: `ListView` and `DetailView`
    * Class-based views : https://docs.djangoproject.com/en/4.1/ref/class-based-views/
* The DetailView generic view expects the primary key value captured from the URL to be called "pk"
* By default, the DetailView generic view uses a template called `<app name>/<model name>_detail.html`
    * For the ListView, `<app name>/<model name>_list.html`
