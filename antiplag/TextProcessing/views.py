"""
Definition of views.
"""
from .models import Text
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.http import HttpResponseRedirect
from .tasks import adding_task


def home(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    all_text = Text.objects.all()
    return render(request,
                  'TextProcessing/text_add.html',
                  {'all_sources': all_text, }
                  )


def account_render(request):
    """Renders the account page."""
    assert isinstance(request, HttpRequest)
    user_texts = Text.objects.filter(author=request.user.username)
    return render(request,
                  'TextProcessing/account.html',
                  {'all_sources': user_texts},
                  )


def create(request):
    assert isinstance(request, HttpRequest)
    text = Text()
    if request.user.is_authenticated:
        text.author = request.user.username
    text.source = request.POST.get("Source")
    text.content = request.POST.get("Content")
    text.save()
    return HttpResponseRedirect("/")


def text_details(request, pk):
    assert isinstance(request, HttpRequest)
    text = Text.objects.filter(id=pk)
    return render(request,
                  'TextProcessing/text_details.html',
                  {'text': text},
                  )


def check_uniqueness(request):
    return HttpResponseRedirect("/")


def celery_check(request):
    adding_task.delay(5, 5)
    return HttpResponse("DONE")
