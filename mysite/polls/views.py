from django.shortcuts import render
from django.http import HttpResponse
from .models import Question

# Index
def index01(request):
    return HttpResponse("Hello, world! You're at polls index.")

def index(request):
    # sort QuerySet using its order_by method. '-pub_date' means descending
    # order
    latest_question_list = Question.objects.order_by('-pub_date')[:5]

    # QuerySet is iterable
    output = ', '.join([q.question_text for q in latest_question_list])
    return HttpResponse(output)

# Get question_id from urls
def detail(request, question_id):
    return HttpResponse("You're looking at question %s." % question_id)

def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)
