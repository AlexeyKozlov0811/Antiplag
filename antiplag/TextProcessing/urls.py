from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^text_catalog$', views.texts, name='texts'),
    url(r'^text_selection$', views.selection, name='selection'),
    url(r'^select_texts/$', views.select_texts, name='select_texts'),
    url(r'^add_text/$', views.add_text, name='process_text'),
    url(r'^account/$', views.account_render, name='account_render'),
    url(r'^text/(?P<pk>\d+)/$', views.text_details),
    url(r'^ajax/validate_username/$', views.validate_username, name='validate_username'),
    url(r'^text_source/(?P<first_text_id>\d+)/(?P<second_text_id>\d+)/$', views.text_source, name='text_source'),
    url(r'^highlight_text/(?P<pk>\d+)/$', views.highlight_text, name='text_source'),
]
