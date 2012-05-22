#-*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('apps.base.views',
    (r'^static$', 'static'),
    (r'^returnToAndroidApp$', 'returnToAndroidApp'),
    (r'^/?$',                      'homepage'),
)
