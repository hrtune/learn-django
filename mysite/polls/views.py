from django.shortcuts import render
from django.http import HttpResponse
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

# Get question_id from urls
def detail(request, question_id):
    return HttpResponse("You're looking at question %s." % question_id)

def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)
