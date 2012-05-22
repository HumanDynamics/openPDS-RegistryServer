#-*- coding: utf-8 -*-


from django.shortcuts import render_to_response, HttpResponse, redirect
from django.template import RequestContext
from oauth2app.models import Client, AccessToken
from django.contrib.auth.decorators import login_required

@login_required
def homepage(request):
    template = {}
    if request.user.is_authenticated():
        clients = Client.objects.filter(user=request.user)
        access_tokens = AccessToken.objects.filter(user=request.user)
        access_tokens = access_tokens.select_related()
        template["access_tokens"] = access_tokens
        template["clients"] = clients
    return render_to_response(
        'base/homepage.html', 
        template, 
        RequestContext(request))
    

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