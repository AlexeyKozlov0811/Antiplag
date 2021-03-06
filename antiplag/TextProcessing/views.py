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


def selection(request):
    """Renders the text selection page."""
    assert isinstance(request, HttpRequest)
    return render(request,
                  'app/selection_page.html',
                  )


def texts(request):
    """Renders the text list page."""
    assert isinstance(request, HttpRequest)
    all_text = Text.objects.all()
    processing_texts = len(all_text.filter(uniqueness=-1.0))
    web_texts = len(all_text.filter(uniqueness=101))
    return render(request,
                  'app/text_catalog.html',
                  {'all_sources': all_text,
                   'processing_texts': processing_texts,
                   'web_texts': web_texts, }
                  )


def account_render(request):
    """Renders the account page."""
    assert isinstance(request, HttpRequest)
    user_texts = Text.objects.filter(author=request.user.username)
    processing_texts = len(user_texts.filter(uniqueness=-1.0))
    return render(request,
                  'app/account.html',
                  {'all_sources': user_texts,
                   'processing_texts': processing_texts, },
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
    return HttpResponseRedirect("/text/" + str(text_id) + '/')


def select_texts(request):
    uniqueness_upper_border = float(request.POST.get("uniqueness_upper_border")),
    uniqueness_upper_border = uniqueness_upper_border[0]
    uniqueness_down_border = float(request.POST.get("uniqueness_down_border")),
    uniqueness_down_border = uniqueness_down_border[0]
    if request.user.is_staff:
        author = request.POST.get("author_texts")
    else:
        author = request.user.username
        if not (0.0 <= uniqueness_upper_border <= 100.0):
            uniqueness_upper_border = 100.0
        if not (0.0 <= uniqueness_down_border <= 100.0):
            uniqueness_down_border = 0.0
    Selection = SelectionRequest(author_filter=author,
                                 key_words_filter=request.POST.get("source_filters").split(' '),
                                 uniqueness_upper_border=uniqueness_upper_border,
                                 uniqueness_down_border=uniqueness_down_border,
                                 left_date=request.POST.get("left_date"),
                                 right_date=request.POST.get("right_date")
                                 )

    success_uniqueness_test_border = float(request.POST.get("uniqueness_success_border"))
    selection_set = Selection.GetSelectionSet()
    set_length = len(selection_set)
    return render(request,
                  'app/selection_set.html',
                  {'SelectionSet': selection_set,
                   'success_uniqueness_test_border': success_uniqueness_test_border,
                   'set_length': set_length},
                  )


def validate_username(request):
    """Answers ajax request check free username."""
    username = request.GET.get('username', None)
    data = {
        'is_taken': User.objects.filter(username__iexact=username).exists()
    }
    return JsonResponse(data)


def text_source(request, first_text_id, second_text_id):
    """Answers ajax request to get text content."""
    if request.is_ajax():
        text_content = GetTextContent(second_text_id)
        text_burrowed_content = GetTextBurrowedContent(first_text_id, second_text_id)
        response = {'text': text_content.rstrip('\n'),
                    'burrowed_content': text_burrowed_content}
        return JsonResponse(response)
    else:
        raise Http404


def highlight_text(request, pk):
    """Answers ajax request to highlight text parts."""
    if request.is_ajax():
        text_burrowed_content = GetTextBurrowedContent(pk)
        # print(text_burrowed_content)
        if text_burrowed_content:
            text_burrowed_content_sources = list(text_burrowed_content.keys())
            response = {'text': text_burrowed_content,
                        'sources': text_burrowed_content_sources}
        else:
            response = None
        return JsonResponse(response, safe=False)
    else:
        raise Http404
