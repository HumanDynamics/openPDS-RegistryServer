from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
from apps.account.api import UserResource
from django.contrib import admin
admin.autodiscover()

user_resource = UserResource()

urlpatterns = patterns('views',
    (r'^', include('apps.base.urls')),
    (r'^account/', include('apps.account.urls')),
    (r'^client/', include('apps.client.urls')),
    (r'^oauth2/', include('apps.oauth2.urls')),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^get_key_from_token$', 'get_key_from_token'),
    (r'^get_user_list$', 'get_user_list'),
#    (r'^get_sid_from_id$', 'get_sid_from_id'),
#    (r'^get_id_from_sid$', 'get_id_from_sid'),
    (r'^oic/', include(user_resource.urls)),
    (r'^get_system_entity_connection$', 'get_system_entity_connection'),
)

#handler404 = 'oauthManagement.regisryServer.apps.api.views.log_404'
#handler403 = 'oauthManagement.regisryServer.apps.api.views.log_403'
#handler500 = 'oauthManagement.regisryServer.apps.api.views.log_500'
#handler401 = 'oauthManagement.regisryServer.apps.api.views.log_401'
    #(r'^api/', include('registryServer.regisryServer.apps.api.urls')),

