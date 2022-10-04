# More views

** Add new views **
`polls/views.py`:
```python
# ...
def detail(request, question_id):
    return HttpResponse("You're looking at question %s." % question_id)

def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)
# ...
```
* All of these take an argument `question_id`.

===

** Route to new views **

`polls/urls.py`:
```python
# ...
urlpatterns = [
    # ex: /polls/
    path('', views.index, name='index'),
    # ex: /polls/5/
    path('<int:question_id>/', views.detail, name='detail'),
    # ex: /polls/5/results/
    path('<int:question_id>/results/', views.results, name='results'),
    # ex: /polls/5/vote/
    path('<int:question_id>/vote/', views.vote, name='vote'),
]
# ...
```
* `<int:question_id>` captures an integer and pass it to the following method as `question_id`.

===

** Write views that actually do something **

```python
# ...
def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    output = ', '.join([q.question_text for q in latest_question_list])
    return HttpResponse(output)
# ...
```

* `Question.objects.order_by('-pub_date')[:5]` 
    * c.f. https://docs.djangoproject.com/en/4.1/ref/models/querysets/#django.db.models.query.QuerySet.order_by
    * `order_by('-pub_date')` means order the QuerySet by 'pub_date' in decending order (denoted by '-')

===

** Make the first template **

`polls/templates/polls/index.html`:
```html
{% if latest_question_list %}
    <ul>
    {% for question in latest_question_list %}
        <li><a href="/polls/{{ question.id }}/">{{ question.question_text }}</a></li>
    {% endfor %}
    </ul>
{% else %}
    <p>No polls are available.</p>
{% endif %}
```
* This template needs to get latest_question_list object from the 'context'
* So many weird curly brackets... c.f. https://docs.djangoproject.com/en/4.1/ref/templates/language/

===
 
** Render the template **

```python
# ...
def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    template = loader.get_template('polls/index.html')
    context = {
        'latest_question_list': latest_question_list,
    }
    return HttpResponse(template.render(context, request))
```
* context used to render
    * means to pass an object to a corresponding key in the template

===

** Use the shortcut: render() **

```python
from django.shortcuts import render
# ...
def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)
# ...
```

===

** Raising a 404 **

```python
from django.http import Http404
# ...
def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, 'polls/detail.html', {'question': question})
# ...
```

===

** get_object_or_404() **

```python
from django.shortcuts import get_object_or_404, render
# ...
def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})
# ...
```

===

** Use the url tag in a template **
In `polls/index.html`:
```html
<!-- ... -->
<li><a href="{% url 'polls:detail' question.id %}">{{ question.question_text }}</a></li>
<!-- ... -->
```
* c.f. https://docs.djangoproject.com/en/4.1/topics/http/urls/#reverse-resolution-of-urls
* syntax : `{ url 'app_name:url_name' value_to_pass }` 

In `polls/urls.py`:
```python
# ...
app_name = 'polls'
urlpatterns = [
# ...
```


