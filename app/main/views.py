from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    context = {
        'title': "Home",
    }
    return render(request, 'main/index.html', context)
    #return HttpResponse("Home page")

def vostreb(request):
    context = {
        'title': "Vostreb",
    }
    return render(request, 'main/vostreb.html', context)
    #return HttpResponse("Home page")
def skills(request):
    context = {
        'title': "skills",
    }
    return render(request, 'main/skills.html', context)
    #return HttpResponse("Home page")
def last_vac(request):
    context = {
        'title': "last_vac",
    }
    return render(request, 'main/last_vac.html', context)
    #return HttpResponse("Home page")
def georgraph(request):
    context = {
        'title': "georgraph",
    }
    return render(request, 'main/georgraph.html', context)
    #return HttpResponse("Home page")
# Create your views here.
