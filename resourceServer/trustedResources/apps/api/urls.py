#-*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, include, url
import logging, random, hashlib, string

urlpatterns = patterns('trustedResources.apps.api.views',
    (r'^data$',                 'data'),
    (r'^set_role_permissions$',     'setRolePermissions'),
    (r'^set_sharing_level$',     'changeSharingLevel'),
    (r'^set_funf_sensor_groups$',     'changeFunfConfig'),
    (r'^getDefaults$',     'getDefaults'),
    (r'^get_answers$',	'viz'),
    (r'^get_results$', 'viz'),
    (r'^set_funf_data$', 'data'),
    (r'^get_funf_sensor_data$', 'getFunfSensorData'),
    (r'^set_reality_analysis_data$', 'setRealityAnalysisData'),
    (r'^get_reality_analysis_data$', 'getRealityAnalysisData'),
    (r'^delete_reality_analysis_data$', 'deleteRealityAnalysisData'),
    (r'^update_reality_analysis_data$', 'updateRealityAnalysisData'),

)

