from django.shortcuts import render
from . import app8

def index(request):
    return render(request, "dash_sample/index.html")

