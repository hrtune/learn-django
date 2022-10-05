from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.views import generic
from django.urls import reverse
from .models import Question, Choice


# ------ Index ------

# the simplest one
def index01(request):
    return HttpResponse("Hello, world! You're at polls index.")

# hard-coded response
def index02(request):
    # sort QuerySet using its order_by method. '-pub_date' means descending
    # order
    latest_question_list = Question.objects.order_by('-pub_date')[:5]

    # QuerySet is iterable
    output = ', '.join([q.question_text for q in latest_question_list])
    return HttpResponse(output)

# Render using a template and context
def index03(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    template = loader.get_template('polls/index.html')
    context = {
        'latest_question_list': latest_question_list,
    }
    return HttpResponse(template.render(context, request))

# Render using a shortcut render()
def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)

# class-based index
class IndexView(generic.ListView):
    template_name = 'polls/index.html'

    # object name in the template
    # the default is 'question_list' (where 'modelName_list')
    context_object_name = 'latest_question_list'

    # pass this object to the template 
    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]



# ------ Detail ------

# simplest one
def detail01(request, question_id):
    return HttpResponse("You're looking at question %s." % question_id)

# Raise 404 if there is no such question
def detail02(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, 'polls/detail.html', {'question': question})

# If failed to get, return 404 response
def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})

# class-based detail
class DetailView(generic.DetailView):
    # the default context_object_name is question (if Model then model)
    model = Question
    template_name = 'polls/detail.html'


# ------ Results ------
def results01(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})

# class-based results
class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'




# vote
def vote01(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)

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
