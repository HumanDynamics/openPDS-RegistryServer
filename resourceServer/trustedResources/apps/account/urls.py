#-*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('oauthManagement.apps.account.views',
    (r'^logout/?$',                 'logout'),
    (r'^signup/?$',                 'signup'),
    (r'^clients/?$',                'clients'),
    (r'^role_users/([1234567890]+)/?$',             'roleUsers'),
    (r'^remove_role/([1234567890]+)/([1234567890]+)/(.*)$',             'removeRole'),
    (r'^admin_toolbar/?$',            'adminToolbar'),
    (r'^admin_panel/?$',            'adminToolbar'),
)
urlpatterns += patterns('',
  (r'^login/?$',                  'django.contrib.auth.views.login', {'template_name': 'account/login.html'}),
)
