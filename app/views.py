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
from .DataProcessing.Parser import get_content, find_text_urls
from .DataProcessing.shingling import compaire_texts


# def home(request):
#     """Renders the home page."""
#     assert isinstance(request, HttpRequest)
#     return render(
#         request,
#         'app/index.html',
#         {
#             'title': 'Home Page',
#             # 'year': datetime.now().year,
#         }
#     )


def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title': 'Contact',
            'message': 'Your contact page.',
            'year': datetime.now().year,
        }
    )


def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title': 'About',
            'message': 'Your application description page.',
            'year': datetime.now().year,
        }
    )

"""Renders the about page."""
def get(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    all_text = Text.objects.all()
    # Text.objects.all().delete()
    return render(
        request,
        'app/text_list.html',
        {
            'all_sources': all_text,
        }
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


def check_uniq(request):
    # text = Text()
    #     # text.source = request.POST.get("Source")
    #     # text.content = request.POST.get("Content")
    sources = 1
    percentage = 100
    # all_text = Text.objects.all()
    # for text2 in all_text:
    #     sources.append(text2.source)
    #     percentage.append(compaire_texts(text.content, text2.content))
    #     # uniq.update({text2.source : percentage})
    #
    # urls = list(set(find_text_urls(text.content)))
    # for i in all_text:
    #     try:
    #         urls.remove(i.source)
    #     except ValueError:
    #         continue
    #
    # sources.extend(urls)
    #
    # for url in urls:
    #     text2 = Text()
    #     text2.source = url
    #     text2.content = get_content(url)
    #     percentage.append(compaire_texts(text.content, text2.content))
    #     # uniq.update({text2.source : percentage})
    #     text2.save()
    #
    # if 100.0 not in percentage:
    #     text.save()
    # return render(request, 'app/uniq.html', {'uniq': sources, 'percentage': percentage})
    return HttpResponseRedirect("/")