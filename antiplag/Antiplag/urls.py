"""
Definition of urls for Antiplag.
"""

from django.conf.urls import url
import django.contrib.auth.views
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings

import TextProcessing.forms
import TextProcessing.views

# Uncomment the next lines to enable the admin:
from django.conf.urls import include
from django.contrib import admin

admin.autodiscover()

urlpatterns = [
    # Examples:
    url(r'^$', TextProcessing.views.home, name='home'),
    url(r'^text$', TextProcessing.views.get, name='text'),
    url(r'^create/$', TextProcessing.views.create, name='create'),
    url(r'^check_uniq/$', TextProcessing.views.check_uniq, name='check_uniq'),
    url(r'^account/$', TextProcessing.views.account_render, name='account_render'),
    url(r'^text/(?P<pk>\d+)/$', TextProcessing.views.text_details),

    url(r'^accounts/', include('allauth.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

]
