"""
Definition of views.
"""
from .models import Text
from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from .DataProcessing import Parser
#from .DataProcessing import DES_crypting


def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Home Page',
            'year':datetime.now().year,
        }
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Contact',
            'message':'Your contact page.',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
        }
    )

def get(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    all_text = Text.objects.all()
    return render(
        request, 
        'app/text_list.html',
        {
            'all_sources':all_text,
        }
    )

def create(request):
    if request.method == "POST":
        text = Text()
        text.source = request.POST.get("Source")
        text.content = request.POST.get("Content")
        text.save()
    return HttpResponseRedirect("/")



