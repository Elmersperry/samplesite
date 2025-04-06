from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

# Контроллеры:
def index(request):
    return HttpResponse("Здесь будет выведен список объявлений.")