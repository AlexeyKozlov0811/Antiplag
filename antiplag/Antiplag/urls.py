"""
Definition of urls for Antiplag.
"""

from django.urls import path, include
from django.contrib import admin

admin.autodiscover()

urlpatterns = [
    path(r'admin/', admin.site.urls),
    path(r'accounts/', include('allauth.urls')),
    path('', include('TextProcessing.urls')),
]
