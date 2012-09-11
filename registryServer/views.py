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



upload_dir = setting.SERVER_DATA_UPLOAD_DIRECTORY

# to be called from a resource server.  This will read a mongo store of an app, and return the results all documents held in the app's mongo store.
def initCollection(request):
    #import pydevd;pydevd.settrace('18.189.24.242',port=5678)
    #scope = AccessRange.objects.get(key="reality_analysis")
    #authenticator = JSONAuthenticator(scope=scope)
    #pk = ""

    #try:
    #    authenticator.validate(request)
    #    pk = str(authenticator.user.pk)
    #except AuthenticationException:
    #    logging.debug(authenticator.error_response())
    #    return authenticator.error_response()

    usr_id = ""
    col_name = ""
    result = list()
    try:
        connection = Connection()
        db = connection['Applications']
        if request.method == 'GET':
            if request.GET.__contains__('user_id'):
                usr_id = str(request.GET['user_id'])
            else:
                raise Exception('missing user_id from GET parameters')
            if request.GET.__contains__('collection_name'):
                col_name = str(request.GET['collection_name'])
#                pds_url = pds_path+"?pk="+pk+"&scope=reality_analysis"
            else:
                raise Exception('missing collection_name from GET parameters')

        result = read_mongo(db, str(col_name))
    except Exception as e:
        result = {'success':False, 'error_message':e.message}
    finally:
        connection.disconnect()
        response_content = json.dumps(result, default=json_util.default)
        response = HttpResponse(
            content=response_content,
            content_type='application/json')
    	return response

#def instantiateUser(user_id):



#Mongo Interface Operations

#Read all documents in a mongo database, for the specified collection, mask, and exclusions.
#
#Input Parameters
#db - an open connection to a mongo database
#collection - a string specifying the mongo collection to read from
#mask - the query mask.  The query will return all documents that fit the mask, minus the parts eliminated by the exclude parameter
#include - a {<"key">: boolean} list of objects, set to 1 if the key should be included, and 0 if included.
#
#Return Elements
#on success - A python-list of python-dictionary items containing the query result.
#on failure - A python-list of python dictionary items containing the failure information.
def read_mongo(db, collection, mask=None,include=None):
    response_list = list()
    try:
        if(collection == "funf_data"):
            query_result = db.funf_data.find()
        elif(collection == "reality_analysis_service"):
            query_result = db.reality_analysis_service.find()
        elif(collection == "personalPermissions"):
            query_result = db.personalPermissions.find()
        elif(collection == "logCollection"):
            query_result = db.logCollection.find()
        else:
    	    raise Exception('message','collection specified is unknown to read_mongo')
	
	for(idx, result) in enumerate(query_result):
	    response_list.append(result)

    except:
	raise Exception('unexpected error in read_mongo')
    return response_list



#entry point for Reality Analysis api
def reality_analysis(request):
    logging.debug('reality_analysis')
    #authenticate REST request
    scope = AccessRange.objects.get(key="reality_analysis")
    authenticator = JSONAuthenticator(scope=scope)
    pk = ""

    try:
        authenticator.validate(request)
        pk = str(authenticator.user.pk)
    except AuthenticationException:
        logging.debug(authenticator.error_response())
        return authenticator.error_response()
    #call resource server for appropriate script
    try:

	if request.method =='GET':
		for param in request.GET:
		    logging.debug(param)
		    logging.debug(request.GET[param])
		conn = httplib.HTTPConnection("dcaps-staging.media.mit.edu", timeout=100)
	
		#strip app indicator and append parms to
		pds_path = request.path.replace('/reality_analysis','').rstrip('/')
		pds_url = pds_path+"?pk="+pk+"&scope=reality_analysis"
		for param in request.GET:
		    pds_url += "&"+param+"="+request.GET[param]
		    
		#make request	
		logging.debug(pds_url)
		conn.request("GET",str(pds_url))
		r1 = conn.getresponse()

		logging.debug(r1.status)
		logging.debug(r1.reason)
		logging.debug(r1.msg)
		response_text = r1.read()
		conn.close()
		logging.debug(response_text)

	if request.method =='POST':
		logging.debug(request.raw_post_data)
		for param in request.POST:
		   logging.debug(param)
		   logging.debug(request.POST[param])
		conn = httplib.HTTPConnection("dcaps-staging.media.mit.edu", timeout=100)
		
		
		#strip app indicator and append parms to
		pds_path = request.path.replace('/reality_analysis','').rstrip('/')
		pds_path += "?pk="+pk+"&scope='reality_analysis'"
		pds_post = ""
		for param in request.POST:
		    pds_post += "&"+param+"="+request.POST[param]
		pds_post = request.raw_post_data    
	
		#make request	
		logging.debug("POSTING...")
		logging.debug(pds_path)
		logging.debug(pds_post)
		conn.request("POST",pds_path,str(pds_post))
		r1 = conn.getresponse()
		r1.status
		r1.reason
		response_text = r1.read()
		conn.close()
		
    except error:
	data = {'error': 'PDS request failed'}
	json_data = json.dumps(data)
	return HttpResponse(content=json_data,
			content_type='application/json')

    return HttpResponse(content=response_text,
			content_type='application/json')



#entry point for Reality Analysis api
def funf_write(request):
    logging.debug('funf_write')
    #authenticate REST request
    scope = AccessRange.objects.get(key="funf_write")
    authenticator = JSONAuthenticator(scope=scope)
    pk = ""

    try:
        authenticator.validate(request)
        pk = str(authenticator.user.pk)
    except AuthenticationException:
        logging.debug(authenticator.error_response())
        return authenticator.error_response()
    #call resource server for appropriate script
    try:

	if request.method =='GET':
		for param in request.GET:
		    logging.debug(param)
		    logging.debug(request.GET[param])
		conn = httplib.HTTPConnection("dcaps-staging.media.mit.edu", timeout=100)
	
		#strip app indicator and append parms to
		pds_path = request.path.replace('/funf_write','').rstrip('/')
		pds_url = pds_path+"?pk="+pk+"&scope='funf_write'"
		for param in request.GET:
		    pds_url += "&"+param+"="+request.GET[param]
		    
		#make request	
		logging.debug(pds_url)
		conn.request("GET",str(pds_url))
		r1 = conn.getresponse()

		logging.debug(r1.status)
		logging.debug(r1.reason)
		logging.debug(r1.msg)
		response_text = r1.read()
		conn.close()
		logging.debug(response_text)

	if request.method =='POST':
		logging.debug(request.raw_post_data)
		for param in request.POST:
		   logging.debug(param)
		   logging.debug(request.POST[param])
		conn = httplib.HTTPConnection("dcaps-staging.media.mit.edu", timeout=100)
		
		
		#strip app indicator and append parms to
		pds_path = request.path.replace('/funf_write','').rstrip('/')
		pds_url = pds_path+"?pk="+pk+"&scope='funf_write'"
		pds_post = ""
		for param in request.POST:
		    pds_post += "&"+param+"="+request.POST[param]
		pds_post = request.raw_post_data    
		#if request.GET.__contains__('probe'):
		#    pds_url += "&probe="+request.GET['probe']
	
		#make request	
		logging.debug("POSTING...")
		logging.debug(pds_path)
		logging.debug(pds_post)
		conn.request("POST",pds_url,str(pds_post))
		r1 = conn.getresponse()
		r1.status
		r1.reason
		response_text = r1.read()
		conn.close()
		
    except error:
	data = {'error': 'PDS request failed'}
	json_data = json.dumps(data)
	return HttpResponse(content=json_data,
			content_type='application/json')

    return HttpResponse(content=response_text,
			content_type='application/json')


#entry point for Reality Analysis Service api
def reality_analysis_service(request):
    logging.debug("reality_analysis_service")
    #authenticate REST request
    scope = AccessRange.objects.get(key="reality_analysis_service")
    authenticator = JSONAuthenticator(scope=scope)
    pk = ""

    try:
        authenticator.validate(request)
        pk = str(authenticator.user.pk)
    except AuthenticationException:
        logging.debug(authenticator.error_response())
        return authenticator.error_response()
    #call resource server for appropriate script
    try:
	conn = httplib.HTTPConnection("dcapsdev.media.mit.edu", timeout=100)

	#strip app indicator and append parms to
	pds_path = request.path.replace('/reality_analysis_service','').rstrip('/')
	if request.GET.__contains__('probe'):
	    pds_url = pds_path+"?pk="+pk+"&scope='reality_analysis_service'&probe="+request.GET['probe']

	#make request	
	if request.method =='GET':
		for param in request.GET:
		    logging.debug(param)
		    logging.debug(request.GET[param])
		conn = httplib.HTTPConnection("dcaps-staging.media.mit.edu", timeout=100)
	
		#strip app indicator and append parms to
		pds_path = request.path.replace('/reality_analysis_service','').rstrip('/')
		pds_url = pds_path+"?pk="+pk+"&scope='reality_analysis_service'"
		for param in request.GET:
		    pds_url += "&"+param+"="+request.GET[param]
		    
		#make request	
		logging.debug(pds_url)
		conn.request("GET",str(pds_url))
		r1 = conn.getresponse()

		logging.debug(r1.status)
		logging.debug(r1.reason)
		logging.debug(r1.msg)
		response_text = r1.read()
		conn.close()
		logging.debug(response_text)

	if request.method =='POST':
		logging.debug(request.raw_post_data)
		for param in request.POST:
		   logging.debug(param)
		   logging.debug(request.POST[param])
		conn = httplib.HTTPConnection("dcaps-staging.media.mit.edu", timeout=100)
		
		
		#strip app indicator and append parms to
		pds_path = request.path.replace('/reality_analysis_service','').rstrip('/')
		pds_path += "?pk="+pk+"&scope='reality_analysis_service'"
		pds_post = ""
		for param in request.POST:
		    pds_post += "&"+param+"="+request.POST[param]
		pds_post = request.raw_post_data    
		#if request.GET.__contains__('probe'):
		#    pds_url += "&probe="+request.GET['probe']
	
		#make request	
		logging.debug("POSTING...")
		logging.debug(pds_path)
		logging.debug(pds_post)
		conn.request("POST",pds_path,str(pds_post))
		r1 = conn.getresponse()
		r1.status
		r1.reason
		response_text = r1.read()
		conn.close()


    except error:
	data = {'error': 'PDS request failed'}
	json_data = json.dumps(data)
	return HttpResponse(content=json_data,
			content_type='application/json')

    return HttpResponse(content=response_text,
			content_type='application/json')



def log_401(request):
   return {"error": "four o one"}

def log_403(request):
    logging.debug('log 403')
    
    #validate REST
    #scope = AccessRange.objects.get(key="reality_analysis")
    #authenticator = JSONAuthenticator(scope=scope)

    #try:
    #    authenticator.validate(request)
    #except AuthenticationException:
#	logging.debug(authenticator.error__))
#        return authenticator.error_response()
    #datastore_owner = ""
    try:
        datastore_owner = request.GET['datastore_owner']
    except:
        return authenticator.response({"success":False, "reason": "missing datastore_owner"})
	

    #pk = str(authenticator.user.pk)
    #logging.debug(pk)
    #validate permissions
    pk = "1"
    try:
	# connecting to Mongo
	connection = pymongo.Connection()
	db = connection["TF"]
        logCollection = db.log
	al_entry = {}
       	if request.GET.__contains__('purpose'):
       	    al_entry['purpose'] = request.GET['purpose']
	if request.GET.__contains__('script'):
   	    al_entry['script'] = request.path
	if request.GET.__contains__('scope'):
	    al_entry['scope'] = str(scope)
	if request.GET.__contains__('system_entity_toggle'):
	    al_entry['system_entity_toggle'] = True
	else:
	    al_entry['system_entity_toggle'] = False
	# the requester must be the datastore_owner
	if request.GET.__contains__('datastore_owner'):
	    al_entry['datastore_owner'] = datastore_owner 
	if request.GET.__contains__('requester'):
	    al_entry['requester'] = pk 
	if request.GET.__contains__('allow'):
   	    al_entry['trust_wrapper_result'] = 'allow'	
	logCollection.insert(al_entry)
    finally:
        connection.disconnect()
        return authenticator.response({
            "success":True, "error":"Page not found"})
    return authenticator.response({ "success": False})


def log_500(request):
    logging.debug('log 500')
    
    #validate REST
    scope = AccessRange.objects.get(key="reality_analysis")
    authenticator = JSONAuthenticator(scope=scope)

    try:
        authenticator.validate(request)
    except AuthenticationException:
	logging.debug(authenticator.error_response())
        return authenticator.error_response()
    datastore_owner = ""
    try:
        datastore_owner = request.GET['datastore_owner']
    except:
        return authenticator.response({"success":False, "reason": "missing datastore_owner"})
	

    pk = str(authenticator.user.pk)
    logging.debug(pk)
    #validate permissions
    try:
	# connecting to Mongo
	connection = pymongo.Connection()
	db = connection["TF"]
        logCollection = db.log
	al_entry = {}
       	if request.GET.__contains__('purpose'):
       	    al_entry['purpose'] = request.GET['purpose']
	if request.GET.__contains__('script'):
   	    al_entry['script'] = request.path
	if request.GET.__contains__('scope'):
	    al_entry['scope'] = str(scope)
	if request.GET.__contains__('system_entity_toggle'):
	    al_entry['system_entity_toggle'] = True
	else:
	    al_entry['system_entity_toggle'] = False
	# the requester must be the datastore_owner
	if request.GET.__contains__('datastore_owner'):
	    al_entry['datastore_owner'] = datastore_owner 
	if request.GET.__contains__('requester'):
	    al_entry['requester'] = pk 
	if request.GET.__contains__('allow'):
   	    al_entry['trust_wrapper_result'] = 'allow'	
	logCollection.insert(al_entry)
    finally:
        connection.disconnect()
        return authenticator.response({
            "success":True, "error":"Page not found"})
    return authenticator.response({ "success": False})

def log_404(request):
    logging.debug('log 404')
    
    #validate REST
    scope = AccessRange.objects.get(key="reality_analysis")
    authenticator = JSONAuthenticator(scope=scope)

    try:
        authenticator.validate(request)
    except AuthenticationException:
	logging.debug(authenticator.error_response())
        return authenticator.error_response()
    datastore_owner = ""
    try:
        datastore_owner = request.GET['datastore_owner']
    except:
        return authenticator.response({"success":False, "reason": "missing datastore_owner"})
	

    pk = str(authenticator.user.pk)
    logging.debug(pk)
    #validate permissions
    try:
	# connecting to Mongo
	connection = pymongo.Connection()
	db = connection["TF"]
        logCollection = db.log
	al_entry = {}
       	if request.GET.__contains__('purpose'):
       	    al_entry['purpose'] = request.GET['purpose']
	if request.GET.__contains__('script'):
   	    al_entry['script'] = request.path
	if request.GET.__contains__('scope'):
	    al_entry['scope'] = str(scope)
	if request.GET.__contains__('system_entity_toggle'):
	    al_entry['system_entity_toggle'] = True
	else:
	    al_entry['system_entity_toggle'] = False
	# the requester must be the datastore_owner
	if request.GET.__contains__('datastore_owner'):
	    al_entry['datastore_owner'] = datastore_owner 
	if request.GET.__contains__('requester'):
	    al_entry['requester'] = pk 
	if request.GET.__contains__('allow'):
   	    al_entry['trust_wrapper_result'] = 'allow'	
	logCollection.insert(al_entry)
    finally:
        connection.disconnect()
        return authenticator.response({
            "success":True, "error":"Page not found"})
    return authenticator.response({ "success": False})


def isTokenValid(request):
    scope = AccessRange.objects.get(key="funf_write")
    authenticator = JSONAuthenticator(scope=scope)
    try:
        authenticator.validate(request)
    except AuthenticationException:
        return authenticator.error_response()
    return authenticator.response({})
    

    
TMP_FILE_SALT = '2l;3edF34t34$#%2fruigduy23@%^thfud234!FG%@#620k'
TEMP_DATA_LOCATION = "/data/temp/"

def randomHash(pk):
    randstring = "".join([random.choice(string.letters) for x in xrange(20)])
    hash = hashlib.sha224(TMP_FILE_SALT + pk + randstring).hexdigest()[0:40]
    return hash


@csrf_exempt
def error(request):
    return render_to_response("500.html")


def _apiRequest(url, data):
    req = urllib2.Request(url, data)
    response = urllib2.urlopen(req)
    return response.read()


