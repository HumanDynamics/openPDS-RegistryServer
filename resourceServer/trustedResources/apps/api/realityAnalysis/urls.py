#-*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url
import logging, random, hashlib, string

logging.debug('testing urls..')
urlpatterns = patterns('oauthManagement.apps.api.realityAnalysis.views',
    (r'^changeRolePermissions/?$',     'changeRolePermissions'),
    (r'^set_sharing_level/?$',     'changeSharingLevel'),
    (r'^set_funf_config/?$',     'changeFunfConfig'),
    (r'^set_role_permissions/?$',     'setRolePermissions'),
    (r'^viz/$',	'viz'),
    (r'^validate/$', 'isTokenValid'),
    (r'^data/$', 'data'),
    (r'^set_reality_analysis_data/$', 'getResults'),
)

