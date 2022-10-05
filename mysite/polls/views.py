from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from django.template import loader
from .models import Question

# Index
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


# detail
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

def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)
