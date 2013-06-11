#-*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, include, url
import logging, random, hashlib, string

urlpatterns = patterns('apps.generic_connector.views',
    (r'^set_data$',                 'data'),
#    (r'^config$',                 'config'),
#    (r'^setup$',                 'setup'),

)

