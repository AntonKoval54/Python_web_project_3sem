from django.shortcuts import render
from django.http import HttpResponse
from DataForSite.lastvacancieHHAPi import get_lact_vac
from .models import SkillsContent
from .models import GeorgraphContent
from .models import VostrebContent
def index(request):
    context = {
        'title': "Home",
    }
    return render(request, 'main/index.html', context)
    #return HttpResponse("Home page")

def vostreb(request):
    result = VostrebContent.objects.all()
    context = {
        'title': "Vostreb",
        'result': result
    }
    return render(request, 'main/vostreb.html', context)
    #return HttpResponse("Home page")
def skills(request):
    result = SkillsContent.objects.all()
    context = {
        'title': "skills",
        'result': result
    }
    return render(request, 'main/skills.html', context)
    #return HttpResponse("Home page")
def last_vac(request):
    context = {
        'title': "last_vac",
        'vacancies': get_lact_vac()
    }
    return render(request, 'main/last_vac.html', context)
    #return HttpResponse("Home page")
def georgraph(request):
    result = GeorgraphContent.objects.all()
    context = {
        'title': "georgraph",
        'result': result
    }
    return render(request, 'main/georgraph.html', context)
    #return HttpResponse("Home page")
# Create your views here.
