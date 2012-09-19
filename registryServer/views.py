#-*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
import urllib
import urllib2
import hashlib
import datetime

from oauth2app.authenticate import JSONAuthenticator, AuthenticationException
from oauth2app.models import AccessRange
#from account.models import *
from django.http import HttpResponse
import urllib2
import httplib
import logging
#from simplejson import dumps
import pymongo 
from pymongo import Connection
from bson import json_util
import json, ast
import settings


def get_key_from_token(request):
    response_content = {}

    try:
        scope = AccessRange.objects.get(key=str(request.GET['scope']))
        authenticator = JSONAuthenticator(scope=scope)
        authenticator.validate(request)
        response_content['key']=str(authenticator.user.pk)
	response_content['pds_location']=authenticator.user.get_profile().pds_location
	response_content['status']="success"
    except Exception as e:
        response_content['status']="error"
        response_content['message']="failed to get key from token"
	print e

    return HttpResponse(json.dumps(response_content), mimetype="application/json")

def scope_info(request):
    response_data = {}
    try:
	
        accessranges = AccessRange.objects.all()


        response_data['status']="success"
        scope_list = list()
        for accessrange in accessranges:
            scope = {}
            scope['key'] = accessrange.key
            scope['description'] = accessrange.description
            scope_list.append(scope)
        response_data['scope']=scope_list
    except Exception as e:
        response_data['status']="error"
        response_data['message']="Failed to get key from token"
    return HttpResponse(json.dumps(response_data), mimetype="application/json")


def get_user_list(request):
    user_ids = list()
    profs = Profile.objects.all()
    for p in profs:
        user_ids.append(p.id)

    json_dic = {"users":user_ids}
    response_content = json.dumps(json_dic)
    response = HttpResponse(
        content=response_content,
        content_type='application/json')
    return response

def get_sid_from_id(request):
    response_data = {}
    try:
        



