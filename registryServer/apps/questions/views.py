#-*- coding: utf-8 -*-

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from oauth2app.models import Client, AccessRange
from django.contrib.admin.views.decorators import staff_member_required
#from datastoreUtils import *
from apps.questions.models import Script
import pymongo
import json


def getquestion(request):
    question_template = request.GET.get('template')
    template = {}

    return render_to_response('questions/'+question_template,
        template,
        RequestContext(request))

def getandroidquestion(request):
    question_template = request.GET.get('template')
    template = {}

    return render_to_response('questions/android/'+question_template,
        template,
        RequestContext(request))

def update(request):
    s = None
    try:
	s = Script.objects.get(id=request.POST.get('id'))
        s.code = request.POST.get('code')
    except:
	s = Script(name=request.POST.get('name'), code=request.POST.get('code'))
    s.save()
    return HttpResponse(request.body, 'application/json')

def ask(request):
    question_id = request.GET.get('question_id')
    scripts = Script.objects.all()
    template = {"pds_location": "localhost:8003",
		"scripts": scripts}

    if request.method == 'POST':
	print "post please implement"
    
    return render_to_response('questions/ask/'+question_id+'.html',
        template,
        RequestContext(request))
