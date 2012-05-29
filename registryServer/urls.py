from django.conf.urls.defaults import patterns, include, url
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('views',
    (r'^', include('apps.base.urls')),
    (r'^account/', include('apps.account.urls')),
    (r'^client/', include('apps.client.urls')),
    (r'^oauth2/', include('apps.oauth2.urls')),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^api/reality_analysis/\w+', 'reality_analysis'),
    (r'^api/funf_write/\w+', 'funf_write'),
    (r'^api/reality_analysis_service/\w+', 'reality_analysis_service'),
    (r'^RPC2$', 'rpc4django.views.serve_rpc_request'),
    (r'^initialize$', 'initCollection'),
)

#handler404 = 'oauthManagement.apps.api.views.log_404'
#handler403 = 'oauthManagement.apps.api.views.log_403'
#handler500 = 'oauthManagement.apps.api.views.log_500'
#handler401 = 'oauthManagement.apps.api.views.log_401'
    #(r'^api/', include('registryServer.apps.api.urls')),

