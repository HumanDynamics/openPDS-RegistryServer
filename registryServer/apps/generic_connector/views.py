#-*- coding: utf-8 -*- 
import urllib, urllib2, httplib, hashlib, datetime, os, logging
import random, hashlib, string, pymongo, json, ast, sys, settings, requests
import sqlite3, shutil, time, apps.oauth2
from django.http import HttpResponse, HttpResponseBadRequest
from django.utils import simplejson as json_simple
from pymongo import Connection
from bson import json_util
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect, render_to_response
from django.utils.http import urlencode
from oauth2app.authenticate import Authenticator, AuthenticationException, JSONAuthenticator
from oauth2app.models import AccessRange, AccessToken
from django.contrib.auth.decorators import login_required

upload_dir = settings.SERVER_UPLOAD_DIR

def insert_pds(profile, token, pds_json):
    try:
        # get pds location and user id
	    request_path= "http://"+str(profile.pds_location)+"/api/personal_data/generic/?format=json&bearer_token="+str(token)+"&datastore_owner__uuid="+str(profile.uuid)
	    payload = json.dumps(pds_json)
	    r = requests.post(request_path, data=payload, headers = { "content-type" : "application/json" })
	    response = r.text

    except Exception as ex:
	    raise Exception(ex)

    return response
 

def data(request):
    '''upload database files to your PDS'''
    result = {}
    connection = None

    for filename, file in request.FILES.items():
        logging.debug(filename)
    if request.method == 'GET':
        template = {'token':request.GET['bearer_token']}
        return render_to_response('upload.html', template, RequestContext(request))

    pds = None
    scope = AccessRange.objects.get(key="funf_write")
    authenticator = JSONAuthenticator(scope=scope)
    try:
        # Validate the request.
        authenticator.validate(request)
    except AuthenticationException as e:
        # Return an error response.
        print e
        return authenticator.error_response(content="You didn't authenticate.")
    profile = authenticator.user.get_profile()

    try:
        scope = 'funf_write'
        token = request.GET['bearer_token']
        try:
            file_path = upload_dir + file.name
            write_file(str(file_path), file)
        except Exception as ex:
            print "failed to write file to "+file_path+".  Please make sure you have write permission to the directory set in settings.SERVER_UPLOAD_DIR"
        con = sqlite3.connect(file_path)
        cur = con.cursor()
        cur.execute("select * from data")
        inserted = []
        for row in cur:
            # Insert into PDS
            pds_data={}
            pds_data['value']=row
            insert_pds(profile, token, pds_data)
            print "*"*100
            print "inserting row..."
            print pds_data
            print "*"*100
            inserted.append(convert_string(pds_data)+'\n')
        result = {'success': True, 'message':''.join(inserted)} 
    except Exception as e:
        result = {'success':False, 'error_message':e.message}
    finally:
        response_dict = {"status":"success"}
        return HttpResponse(json.dumps(response_dict), content_type='application/json')


def write_file(filename, file):
    if not os.path.exists(upload_dir):
        os.mkdir(upload_dir)
    filepath = os.path.join(upload_dir, filename)
    if os.path.exists(filepath):
        backup_file(filepath)
    with open(filepath, 'wb') as output_file:
        while True:
            chunk = file.read(1024)
            if not chunk:
                break
            output_file.write(chunk)

def backup_file(filepath):
    shutil.move(filepath, filepath + '.' + str(int(time.time()*1000)) + '.bak')


def convert_string(s):
    return "%s" % s

