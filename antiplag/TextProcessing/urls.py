from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^text_catalog$', views.texts, name='texts'),
    url(r'^create/$', views.create_text, name='create'),
    url(r'^process_text/$', views.process_text, name='process_text'),
    url(r'^account/$', views.account_render, name='account_render'),
    url(r'^text/(?P<pk>\d+)/$', views.text_details),
]