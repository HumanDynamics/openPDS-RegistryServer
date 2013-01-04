#-*- coding: utf-8 -*-
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import auth
from apps.account.models import Profile 
from oauth2app.models import Client
import json

def members(request):
    clients = Client.objects.all()
    profiles = Profile.objects.all()
    template = {}
    response_data = {}

    profile_list = list()
    for p in profiles:
        profile_json = {}
        profile_json['location'] = str(p.pds_ip)+":"+str(p.pds_port)
        profile_json['user'] = p.user.username
        profile_json['uuid'] = p.uuid
        profile_list.append(profile_json)

    response_data['profiles']=profile_list
    return HttpResponse(json.dumps(response_data), mimetype="application/json")

