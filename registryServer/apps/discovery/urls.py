#-*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url, include

urlpatterns = patterns('apps.discovery.views',
    (r'^members', 'members'),
)

