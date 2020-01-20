"""
Module contains controller logic
"""

from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import HttpRequest, HttpResponseRedirect, JsonResponse, Http404
from .tasks import check_uniqueness
from .services.TextService import *


def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(request,
                  'app/home_page.html',
                  )


def texts(request):
    """Renders the text list page."""
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


def text_details(request, pk):
    """Renders the text details page."""
    assert isinstance(request, HttpRequest)
    text = Text.objects.filter(id=pk)
    return render(request,
                  'app/text_details.html',
                  {'text': text},
                  )


def add_text(request):
    author = "Unknown"
    content = request.POST.get("Content")
    if request.user.is_authenticated:
        author = request.user.username
    text_id = CreateText(content, author)
    check_uniqueness.delay(text_id)
    return HttpResponseRedirect("/")


def validate_username(request):
    """Answers ajax request check free username."""
    username = request.GET.get('username', None)
    data = {
        'is_taken': User.objects.filter(username__iexact=username).exists()
    }
    return JsonResponse(data)


def text_source(request, pk):
    """Answers ajax request to get text content."""
    if request.is_ajax():
        text_content = GetTextContent(pk)
        response = {'text': text_content}
        return JsonResponse(response)
    else:
        raise Http404


def highlight_text(request, pk):
    """Answers ajax request to highlight text parts."""
    if request.is_ajax():
        text_burrowed_content = GetTextBurrowedContent(pk)
        if text_burrowed_content:
            response = {'text': json.loads(text_burrowed_content)}
        else:
            response = {'text': "1"}
        return JsonResponse(response)
    else:
        raise Http404
