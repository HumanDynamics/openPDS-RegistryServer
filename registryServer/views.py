#-*- coding: utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
import urllib
import urllib2
import hashlib
import datetime
import requests

from oauth2app.authenticate import JSONAuthenticator, AuthenticationException, Authenticator, InsufficientScope
from oauth2app.models import AccessRange
from django.contrib.auth.decorators import login_required
from apps.account.models import UserToUser, User, Profile
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
from django.shortcuts import render_to_response


def redirect(request):
    return HttpResponse("")

def isup(request):
    response = {"success":True}
    return HttpResponse(json.dumps(response), mimetype="application/json")

def js(request):
    response = {"success":True}
    return render_to_response('javascript/test.js' )

def members(request):
    profiles = Profile.objects.all()
    
    template = { "profiles": profiles }
    return render_to_response("members.rdf", template, mimetype="application/rdf+xml")

def get_key_from_token(request):
    response_content = {}

    try:
        scope = AccessRange.objects.get(key=str(request.GET['scope']))
        authenticator = JSONAuthenticator(scope=scope)
        authenticator.validate(request)
        if request.GET.get('hostid'):
            u2u = get_object_or_404(UserToUser,id=request.GET['hostid'])
            #a request from a peer
            role_list = []
            role_list.append(u2u.role)
            response_content['roles'] = role_list
            response_content['request_type'] = "peer"
        else:
            response_content['request_type'] = "self"
            #a request from self (host=guest)
            response_content['key']=authenticator.user.get_profile().uuid
            response_content['pds_location']=authenticator.user.get_profile().pds_location
            response_content['status']="success"
    except Exception as e:
        response_content['status']="error"
        response_content['message']="failed to get key from token:"
        print e

    return HttpResponse(json.dumps(response_content), mimetype="application/json")


def get_system_entity_connection(request):
    response_content = {}

    try:
        scope = AccessRange.objects.get(key="system_entity")
        authenticator = Authenticator(scope=scope)
	authenticator.validate(request)
	if scope not in authenticator.scope:
	    raise Exception("Access token is insufficient to get a system entity connection")
	pdslocationlist = list()
	for user in User.objects.all():
	    pdslocationlist.append(user.get_profile().pds_location)	
        response_content['pds_locations']=pdslocationlist
        response_content['status']="success"
    except Exception as e:
        response_content['status']="error"
        response_content['message']="failed to connect as system entity"
	logging.debug(e)

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

#@login_required
#def init_pds(request):
#    user_ids = list()
#    profs = Profile.objects.all()
#    for p in profs:
#        user_ids.append(p.id)
#
#    profile = request.user.get_profile()
##    scope_url = 'http://'+str(profile.pds_ip)+":"+str(profile.pds_port)+'/api/personal_data/scope/'
##    purpose_url = 'http://'+str(profile.pds_ip)+":"+str(profile.pds_port)+'/api/personal_data/pupose/'
#    role_url = 'http://'+str(profile.pds_ip)+":"+str(profile.pds_port)+'/api/personal_data/role/'
#    r = requests.post(role_url, data=json.dumps({"issharing":True,"name":"Family", "datastore_owner": 2}))
#    r = requests.post(role_url, data=json.dumps({"issharing":True,"name":"Peers", "datastore_owner": 2}))
#    r = requests.post(role_url, data=json.dumps({"issharing":True,"name":"Care_Team", "datastore_owner": 2}))
##    sharinglevel_url = 'http://'+str(profile.pds_ip)+":"+str(profile.pds_port)+'/api/personal_data/sharinglevel/'
##    payload = {'some': 'data'}
#
#    
#
#    json_dic = {"success":True}
#    response_content = json.dumps(json_dic)
#    response = HttpResponse(
#        content=response_content,
#        content_type='application/json')
#    return response


#def get_sid_from_id(request):
#    response_data = {}
#    try:
        



