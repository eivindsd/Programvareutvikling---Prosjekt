from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def home(request):
    """Returns that we have landed on the home-page"""
    return HttpResponse('<h1>Blog Home</h1>')


def about(request):
    """Returns """
    return HttpResponse('<h1>Blog About</h1>')



