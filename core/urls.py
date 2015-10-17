from django.conf.urls import patterns, url
from .tests import echarts
from .views import (index, modal_form, modal_delete, container_page)
urlpatterns = patterns('',
    url(r'^$', index, name='index'),
    url(r'^modal_form/$', modal_form, name="modal_form"),
    url(r'^modal_form/(?P<id>\d+)/$', modal_form, name="modal_form"),
    url(r'^modal_form/(?P<app>[a-z]+)/(?P<form_name>[a-z_]+)/$', modal_form, name='modal_form'),
    url(r'^modal_form/(?P<app>[a-z]+)/(?P<form_name>[a-z_]+)/(?P<id>\d+)/$', modal_form, name='modal_form'),
    url(r'^modal_delete/(?P<app>[a-z]+)/(?P<form_name>[a-z_]+)/(?P<id>\d+)/$', modal_delete, name='modal_delete'),
    url(r'^login/$', 'core.views.login', {'template_name': 'login.html'}),
    url(r'^logout/$', 'django.contrib.auth.views.logout_then_login', name='logout'),
    url(r'^management/(?P<section>[a-z_]+)/$', container_page, name='container_page'),
    url(r'^management/(?P<section>[a-z_]+)/(?P<execute_status>\d+)/$', container_page, name='container_page'),
    url(r'^echarts/$', echarts),


)

