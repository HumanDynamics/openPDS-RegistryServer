#-*- coding: utf-8 -*-

import requests

from django.shortcuts import render_to_response, HttpResponse
from django.template import RequestContext
from oauth2app.models import Client, AccessToken
from django.contrib.auth.decorators import login_required
from django import forms
from apps.account.models import Profile
import settings

class LocationForm(forms.Form):
    location = forms.CharField()

#@login_required
def homepage(request):

    template = { "LOGIN_URL": settings.LOGIN_URL }

    if request.user.is_authenticated():
        user_profile = None
        try:
            user_profile = request.user.get_profile()
        except:
            # On first login, a user will not have a profile...what to do?
            new_profile = Profile()
            new_profile.user = request.user

            new_client = Client(name=request.user.username+"_pds", user=request.user, description="user "+request.user.username+"'s Personal Data Store", redirect_uri="http://"+new_profile.pds_location+"/?username="+request.user.username)
            new_client.save()
            new_profile.pds_client = new_client
            new_profile.save()

        if request.GET.get('location'):
            new_profile = request.user.get_profile()
            new_location = request.GET['location']
            new_profile.pds_location = new_location
            new_profile.save()

        clients = Client.objects.filter(user=request.user)
        access_tokens = AccessToken.objects.filter(user=request.user).select_related()
    #        access_tokens = access_tokens.select_related()
        form = LocationForm()
        #print access_tokens[0].token
        template["access_token"] = access_tokens[0].token if len(access_tokens) > 0 else None
        template["clients"] = clients
        template["profile"] = user_profile
        template['form']=form
        template['isup']=is_pds_up(user_profile)

    return render_to_response(
        'base/homepage.html',
        template,
        RequestContext(request))


def _read_json_success(response):
    """Attempts to read the `success` value from a JSON response, if
    applicable. Returns True or False"""
    if response.status_code != 200:
        return False

    try:
        # requests > 1.0.0
        return response.json().get('success', False)
    except AttributeError:
        # requests < 1.0.0 had a json attribute instead of a method.
        return response.json.get('success', False)


def is_pds_up(profile, request_path="/discovery/ping", schema="http"):
    '''Verifies that a user's PDS is set up and responding'''
    path = "{schema}://{host}{path}".format(
        schema=schema,
        host=profile.pds_location,
        path=request_path
    )
    return _read_json_success(requests.get(path))


#TODO DELETE this section. testing mongoEngine
# handle static pages (such as the About pg, Terms pg, and Privacy policy pg)
from mongoengine import *
class Puser(Document):
    email = StringField(required=True)
    first_name = StringField(max_length=50)
    last_name = StringField(max_length=50)
def static(request):

  connect('project1')#, username='webapp', password='pwd123')
  john = Puser(email='jdoe@example.com', first_name='sfds', last_name='S')
  john.save()
  str = ''
  for p in Puser.objects:
    str += p.first_name + ' ' +p.last_name + '<br/>'
  return HttpResponse(str)

def returnToAndroidApp(request):
    response = HttpResponse(content="", status=302)
    response["Location"] = "my_android_application:///dcapsdev.media.mit.edu/returnToAndroidApp"
    return response#HttpResponseRedirect('mypds-android-app:///dcapsdev.media.mit.edu/returnToAndroidApp')
