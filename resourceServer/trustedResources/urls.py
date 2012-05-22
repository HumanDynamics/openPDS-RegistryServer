from django.conf.urls.defaults import patterns, include, url
from django.conf import settings

#from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns('',
    (r'^api/', include('trustedResources.apps.api.urls')),
)

#handler404 = 'oauthManagement.apps.api.views.log_404'
#handler403 = 'oauthManagement.apps.api.views.log_403'
#handler500 = 'oauthManagement.apps.api.views.log_500'
#handler401 = 'oauthManagement.apps.api.views.log_401'
#    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
#    (r'^admin/', include(admin.site.urls)),
#    (r'^', include('trustedResources.apps.base.urls')),

