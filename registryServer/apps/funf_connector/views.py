#-*- coding: utf-8 -*- 
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
import urllib
import urllib2
import httplib
import hashlib
import datetime
from django.http import HttpResponse, HttpResponseBadRequest
from django.utils import simplejson as json_simple
import logging, random, hashlib, string
import dbmerge, os
from Crypto.Cipher import DES
import pymongo
from pymongo import Connection
import dbdecrypt
import decrypt
import sqlite3
import shutil
import time
from bson import json_util
import json, ast
import sys
import settings
from django.template import RequestContext
from django.shortcuts import redirect
from django.utils.http import urlencode
from oauth2app.authenticate import Authenticator, AuthenticationException, JSONAuthenticator
from oauth2app.models import AccessRange

upload_dir = settings.SERVER_UPLOAD_DIR

def setup(request):
    '''get an OAuth 2.0 token for funf_write scope'''
    #TODO set funf key
    host = request.get_host()
    btoken = None
    client_id = "74b5511428e25655d2bc3a4aa4a794"
    client_secret = "69f9acf42e1e9ce6da9e2fde01c5a2"
    if request.method == 'GET':

	if request.GET.__contains__('bearer_token'):
	    print btoken
	    btoken = request.GET['bearer_token']

	clientstr = "http://"+host+"/connectors/setup"
	client_loc = urlencode({'redirect_uri':clientstr}) 
	
	if request.GET.__contains__('code'):
            # get pds location and user id
            request_path="/oauth2/token?"+client_loc+"&grant_type=authorization_code&client_id="+client_id+"&code="+request.GET['code']
            request_path="http://"+settings.SERVER_OMS_REGISTRY+request_path
            req = urllib2.Request(request_path, "client_secret="+client_secret, {'Content-Type': 'application/json'})
            f = urllib2.urlopen(req)
            response = f.read()
            f.close()
            jresponse = json.loads(response)
            if jresponse.__contains__('access_token'):
                btoken = jresponse['access_token']

	if btoken is not None:
  	    template = {'bearer_token':btoken}
            return render_to_response('funf/set_key.html',
                template,
                RequestContext(request))
	else:
	    return redirect("http://"+settings.SERVER_OMS_REGISTRY+"/oauth2/authorize/?"+client_loc+"&scope=funf_write&response_type=code&client_id="+client_id)
	

    if request.method == 'POST':
        try:
	    print request.body
	    btoken = request.GET['bearer_token']
	    key = request.POST['key']
	    scope = "funf_write"
	    pds = Pds(btoken,scope)
	    json_key = {"key":key}
            insres = insert_pds(pds.location,"api/personal_data/funfconfig/?format=json&token="+str(btoken)+"&scope="+str(scope)+"&multiPDS_user="+str(pds.key),json_key)
	    result = {'status':'success'}
	    response = tfcore.jsonHTTPresponse(result)
	
        except Exception as ex:
	    print "EXCEPTION:"
	    print ex
	
#	return redirect('/connectors/config', bearer_token=btoken)
	sync_string = str(host)+"/connectors/config?bearer_token="+str(btoken)
        template = {"sync_string":sync_string,
			"token":btoken}
        return render_to_response('setup/funf_server_sync.html',
        template,
        RequestContext(request))


    #TODO get funf config
    return HttpResponseBadRequest()


def insert_pds(hostname, path, pds_json):
    # upon success, will return a json {'key':'value'}
    userinfo = {}
    try:
        # get pds location and user id
        request_path=str(hostname)+str(path)
	data = json.dumps(pds_json)
	req = urllib2.Request(request_path, data, {'Content-Type': 'application/json'})
	f = urllib2.urlopen(req)
	response = f.read()
	f.close()

    except Exception as ex:
	raise Exception(ex)
    return response

def write_key(request):
    '''write the password used to encrypt funf database files to your PDS'''
    response = None
    try:
	token = request.GET['bearer_token']
	scope = "funf_write"
	pds = Pds(token,scope)
	pds_data = json.loads(request.body)
	print "POST data"
	print pds_data
        insres = insert_pds(pds.location,"api/personal_data/funfconfig/?format=json&token="+str(token)+"&scope="+str(scope)+"&MultiPDS_user="+str(pds.key),pds_data)
	print insres
	result = {'status':'success'}
	response = tfcore.jsonHTTPresponse(result)
	
    except Exception as ex:
	print "EXCEPTION:"
	print ex
        response = HttpResponseBadRequest('failed to write funf key')
    return response
 

def data(request):
    '''decrypt funf database files, and upload them to your PDS'''
    result = {}
    connection = None

    for filename, file in request.FILES.items():
        logging.debug(filename)
    if request.method == 'GET':
	template = {'token':request.GET['bearer_token']}
    	return render_to_response('upload.html',
        template,
        RequestContext(request))
    pds = None
    scope = AccessRange.objects.get(key="funf_write")
#    authenticator = Authenticator(scope=scope)
    authenticator = JSONAuthenticator(scope=scope)
    try:
        # Validate the request.
        authenticator.validate(request)
    except AuthenticationException as e:
        # Return an error response.
	print e
        return authenticator.error_response(content="You didn't authenticate.")
    profile = authenticator.user.get_profile()
    funf_password = profile.funf_password	
    print funf_password

    try:
	    
        scope = 'funf_write'
	token = request.GET['bearer_token']

	print "starting data upload"
	try:
            key = decrypt.key_from_password(str(funf_password))
	    print key
            file_path = upload_dir + file.name
            write_file(str(file_path), file)
	except Exception as ex:
	    print "failed to write file to "+file_path+".  Please make sure you have write permission to the directory set in settings.SERVER_UPLOAD_DIR"
        dbdecrypt.decrypt_if_not_db_file(file_path, key)
        con = sqlite3.connect(file_path)
        cur = con.cursor()
        cur.execute("select value from data")
	inserted = []
        for row in cur:
	    json_insert = clean_keys(json.JSONDecoder().decode(convert_string(row)))
	    print json_insert
            # Insert into PDS
	    pds_data= {}
	    pds_data['time']=json_insert.get('timestamp')
	    pds_data['value']=json_insert
	    pds_data['key']=json_insert.get('probe')
	    insert_pds("http://"+str(profile.pds_ip)+":"+str(profile.pds_port)+"/","api/personal_data/funf/?format=json&bearer_token="+str(token)+"&scope="+str(scope)+"&datastore_owner="+str(profile.uuid),pds_data)
	    print "inserting row..."
	    print pds_data
	    inserted.append(convert_string(json_insert)+'\n')
	result = {'success': True, 'message':''.join(inserted)} 
			
    except Exception as e:
	print e
        result = {'success':False, 'error_message':e.message}

    finally:
        response_dict = {"status":"success"}
        return HttpResponse(json.dumps(response_dict), content_type='application/json')

    
TMP_FILE_SALT = '2l;3edF34t34$#%2fruigduy23@%^thfud234!FG%@#620k'
TEMP_DATA_LOCATION = "/data/temp/"

def random_hash(pk):
    randstring = "".join([random.choice(string.letters) for x in xrange(20)])
    hash = hashlib.sha224(TMP_FILE_SALT + pk + randstring).hexdigest()[0:40]
    return hash

    
def direct_decrypt(file, key, extension=None):
    assert key != None
    decryptor = DES.new(key) #TODO to make sure the key is 8 bytes long. DES won't accept a shorter key
    encrypted_data = file.read()
    data = decryptor.decrypt(encrypted_data)
    return data


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

def clean_keys(d):
    '''replace all "." with "-" and force keys to lowercase'''
    new = {}
    for k, v in d.iteritems():
        if isinstance(v, dict):
            v = clean_keys(v)
	if isinstance(v, list):
	    for idx,i in enumerate(v):
		if isinstance(i, dict):
       		    v[idx] = clean_keys(i)	
        new[k.replace('.', '-').lower()] = v
    return new


