from django.urls import path

from . import views

urlpatterns = [
    path(r'^$', views.home, name='home'),
    path(r'^text_catalog$', views.texts, name='texts'),
    path(r'^text_selection$', views.selection, name='selection'),
    path(r'^select_texts/$', views.select_texts, name='select_texts'),
    path(r'^add_text/$', views.add_text, name='process_text'),
    path(r'^account/$', views.account_render, name='account_render'),
    path(r'^text/(?P<pk>\d+)/$', views.text_details),
    path(r'^ajax/validate_username/$', views.validate_username, name='validate_username'),
    path(r'^text_source/(?P<first_text_id>\d+)/(?P<second_text_id>\d+)/$', views.text_source, name='text_source'),
    path(r'^highlight_text/(?P<pk>\d+)/$', views.highlight_text, name='text_source'),
]
