from django.conf.urls import url

from . import views

urlpatterns = [
    # url(r'^$', TextProcessing.views.home, name='home'),
    url(r'^$', views.celery_check, name='home'),
    # url(r'^text$', views.get, name='text'),
    url(r'^create/$', views.create, name='create'),
    url(r'^check_uniqueness/$', views.check_uniqueness, name='check_uniq'),
    url(r'^account/$', views.account_render, name='account_render'),
    url(r'^text/(?P<pk>\d+)/$', views.text_details),
]