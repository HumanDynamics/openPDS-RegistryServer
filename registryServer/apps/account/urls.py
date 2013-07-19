#-*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url, include
from apps.account.api import UserResource, ProfileResource, GroupResource, ScopeResource
from tastypie.api import Api

user_resource = UserResource()

v1_api = Api(api_name='v1')
v1_api.register(UserResource())
v1_api.register(ProfileResource())
v1_api.register(GroupResource())
v1_api.register(ScopeResource())

urlpatterns = patterns('apps.account.views',
    (r'^logout/?$',                 'logout'),
    (r'^signup/?$',                 'signup'),
    (r'^clients/?$',                'clients'),
    (r'^role_users/([1234567890]+)/?$',             'roleUsers'),
    (r'^admin_toolbar/?$',            'adminToolbar'),
    (r'^admin_panel/?$',            'adminToolbar'),
#    (r'^json_auth$',	'json_auth'),
    (r'^api/', include(v1_api.urls)),
    (r'^profiles', 'profiles'),
    (r'^members', 'members'),
)
urlpatterns += patterns('',
  (r'^login/?$',                  'django.contrib.auth.views.login', {'template_name': 'account/login.html'}),
)

