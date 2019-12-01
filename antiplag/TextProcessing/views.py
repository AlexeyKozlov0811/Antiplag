"""
Definition of views.
"""
from .models import Text
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from .tasks import check_uniqueness


def home(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    all_text = Text.objects.all()
    return render(request,
                  'app/text_add.html',
                  {'all_sources': all_text, }
                  )


def texts(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    all_text = Text.objects.all()
    return render(request,
                  'app/text_catalog.html',
                  {'all_sources': all_text, }
                  )


def account_render(request):
    """Renders the account page."""
    assert isinstance(request, HttpRequest)
    user_texts = Text.objects.filter(author=request.user.username)
    return render(request,
                  'app/account.html',
                  {'all_sources': user_texts},
                  )


def create_text(request):
    assert isinstance(request, HttpRequest)
    text = Text()
    if request.user.is_authenticated:
        text.author = request.user.username
    text.content = request.POST.get("Content")
    text.save()
    return text


def text_details(request, pk):
    assert isinstance(request, HttpRequest)
    text = Text.objects.filter(id=pk)
    return render(request,
                  'app/text_details.html',
                  {'text': text},
                  )


def process_text(request):
    text = create_text(request)
    check_uniqueness.delay(text.id)
    return HttpResponseRedirect("/")

