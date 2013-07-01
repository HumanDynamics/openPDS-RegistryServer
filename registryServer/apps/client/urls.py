#-*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('',)#-*- coding: utf-8 -*-


from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('apps.client.views',
    (r'^(?P<client_id>\w+)/?$',            'client'),
#    (r"^targeting$", "targeting"),
)# Create your views here.
