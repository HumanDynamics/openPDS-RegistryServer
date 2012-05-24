#-*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, include, url
import logging, random, hashlib, string

urlpatterns = patterns('trustedResources.apps.api.views',
    (r'^data$',                 'data'),
    (r'^changeRolePermissions/?$',     'changeRolePermissions'),
    (r'^changeSharingLevel/?$',     'changeSharingLevel'),
    (r'^changeFunfConfig/?$',     'changeFunfConfig'),
    (r'^getDefaults/?$',     'getDefaults'),
    (r'^viz/$',	'viz'),
    (r'^validate/$', 'isTokenValid'),
    (r'^get_results$', 'getResults'),
)
#handler404 = 'oauthManagement.apps.api.views.my_custom_404_view'
logging.debug('testing urls...not found')

