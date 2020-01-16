"""
Definition of views.
"""
from .models import Text
from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import HttpRequest, HttpResponseRedirect, JsonResponse, HttpResponse, Http404
import json
from .tasks import check_uniqueness


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
    """Adds text to the database."""
    text = Text()
    if request.user.is_authenticated:
        text.author = request.user.username
    text.content = request.POST.get("Content")
    text.save()
    check_uniqueness.delay(text.id)
    return HttpResponseRedirect("/")


def validate_username(request):
    username = request.GET.get('username', None)
    data = {
        'is_taken': User.objects.filter(username__iexact=username).exists()
    }
    return JsonResponse(data)


def text_source(request, pk):
    if request.is_ajax():
        text = Text.objects.get(id=pk)
        response = {'text': text.hide_separators()}
        return JsonResponse(response)
    else:
        raise Http404


def highlight_text(request, pk):
    if request.is_ajax():
        text = Text.objects.get(id=pk)
        if not text.uniqueness == -1:
            response = {'text': json.loads(text.burrowed_content)}
        else:
            response = {'text': ""}
        return JsonResponse(response)
    else:
        raise Http404
