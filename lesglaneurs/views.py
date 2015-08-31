#-*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response

# Create your views here.
def home(request):
    return render(request, 'home.html')

def quiz_typeform(request):
    return render(request, 'quiz_typeform.html')