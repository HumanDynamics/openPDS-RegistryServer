#-*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
import urllib
import urllib2
import hashlib
import datetime
import numpy as np

from django.http import HttpResponse

from trustWrapper import *
from django.utils import simplejson as json_simple
import logging, random, hashlib, string
#from decrypt import directDecrypt
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
#import xmlrpclib

upload_dir = '/data/temp'


class MissingParameterError(Exception):
	def __init__(self, value):
		self.value = value
		self.message = value
	def __str__(self):
		return repr(self.value)


def initializeDatastore(user_id):
    #import pydevd;pydevd.settrace('18.189.24.242',port=5678)
    # initialzes the user's PDS through calls to the registrySerer
    collection = 'personalPermissions'
    conn = httplib.HTTPConnection(registryServer, timeout=100)
    request_path="/initialize?user_id="+str(user_id)+"&collection_name="+str(collection)
    conn.request("GET",str(request_path))
    r1 = conn.getresponse()
    response_text = r1.read()
    conn.close()

    connection = pymongo.Connection()
    db = connection['User_'+str(user_id)]
    insert_string = json.loads(response_text)

    write_mongo(db,collection,insert_string)


    return response_text




def log_401(request):
   return {"error": "four o one"}

#def log_403(request):
#    logging.debug('log 403')
#    
#    try:
#        datastore_owner = request.GET['datastore_owner']
#    except:
#        return authenticator.response({"success":False, "reason": "missing datastore_owner"})
#	
#
#    #pk = str(authenticator.user.pk)
#    #logging.debug(pk)
#    #validate permissions
#    pk = "1"
#    try:
#	# connecting to Mongo
#	connection = pymongo.Connection()
#	db = connection["TF"]
#        logCollection = db.log
#	al_entry = {}
#       	if request.GET.__contains__('purpose'):
#       	    al_entry['purpose'] = request.GET['purpose']
#	if request.GET.__contains__('script'):
#   	    al_entry['script'] = request.path
#	if request.GET.__contains__('scope'):
#	    al_entry['scope'] = str(scope)
#	if request.GET.__contains__('system_entity_toggle'):
#	    al_entry['system_entity_toggle'] = True
#	else:
#	    al_entry['system_entity_toggle'] = False
#	# the requester must be the datastore_owner
#	if request.GET.__contains__('datastore_owner'):
#	    al_entry['datastore_owner'] = datastore_owner 
#	if request.GET.__contains__('requester'):
#	    al_entry['requester'] = pk 
#	if request.GET.__contains__('allow'):
#   	    al_entry['trust_wrapper_result'] = 'allow'	
#	logCollection.insert(al_entry)
#    finally:
#        connection.disconnect()
#        return authenticator.response({
#            "success":True, "error":"Page not found"})
#    return authenticator.response({ "success": False})
#
#
#def log_500(request):
#    logging.debug('log 500')
#    
#    #validate permissions
#    try:
#	# connecting to Mongo
#	connection = pymongo.Connection()
#	db = connection["TF"]
#        logCollection = db.log
#	al_entry = {}
#       	if request.GET.__contains__('purpose'):
#       	    al_entry['purpose'] = request.GET['purpose']
#	if request.GET.__contains__('script'):
#   	    al_entry['script'] = request.path
#	if request.GET.__contains__('scope'):
#	    al_entry['scope'] = str(scope)
#	if request.GET.__contains__('system_entity_toggle'):
#	    al_entry['system_entity_toggle'] = True
#	else:
#	    al_entry['system_entity_toggle'] = False
#	# the requester must be the datastore_owner
#	if request.GET.__contains__('datastore_owner'):
#	    al_entry['datastore_owner'] = datastore_owner 
#	if request.GET.__contains__('requester'):
#	    al_entry['requester'] = pk 
#	if request.GET.__contains__('allow'):
#   	    al_entry['trust_wrapper_result'] = 'allow'	
#	logCollection.insert(al_entry)
#    finally:
#        connection.disconnect()
#        return authenticator.response({
#            "success":True, "error":"Page not found"})
#    return authenticator.response({ "success": False})

#def log_404(request):
#    logging.debug('log 404')
#    
#    #validate REST
#    scope = AccessRange.objects.get(key="reality_analysis")
#    authenticator = JSONAuthenticator(scope=scope)
#
#    try:
#        authenticator.validate(request)
#    except AuthenticationException:
#	logging.debug(authenticator.error_response())
#        return authenticator.error_response()
#    datastore_owner = ""
#    try:
#        datastore_owner = request.GET['datastore_owner']
#    except:
#        return authenticator.response({"success":False, "reason": "missing datastore_owner"})
#	
#
#    pk = str(authenticator.user.pk)
#    logging.debug(pk)
#    logging.debug('pre-get_averages query')
#    #validate permissions
#    try:
#	# connecting to Mongo
#	connection = pymongo.Connection()
#	db = connection["TF"]
#        logCollection = db.log
#	al_entry = {}
#       	if request.GET.__contains__('purpose'):
#       	    al_entry['purpose'] = request.GET['purpose']
#	if request.GET.__contains__('script'):
#   	    al_entry['script'] = request.path
#	if request.GET.__contains__('scope'):
#	    al_entry['scope'] = str(scope)
#	if request.GET.__contains__('system_entity_toggle'):
#	    al_entry['system_entity_toggle'] = True
#	else:
#	    al_entry['system_entity_toggle'] = False
#	# the requester must be the datastore_owner
#	if request.GET.__contains__('datastore_owner'):
#	    al_entry['datastore_owner'] = datastore_owner 
#	if request.GET.__contains__('requester'):
#	    al_entry['requester'] = pk 
#	if request.GET.__contains__('allow'):
#   	    al_entry['trust_wrapper_result'] = 'allow'	
#	logCollection.insert(al_entry)
#    finally:
#        connection.disconnect()
#        return authenticator.response({
#            "success":True, "error":"Page not found"})
#    return authenticator.response({ "success": False})

def setRealityAnalysisData(request):
    logging.debug('set reality analysis data')
    #import pydevd;pydevd.settrace('18.189.24.242',port=5678)
    try:
	connection = pymongo.Connection()
	pk = ""
        if request.GET.__contains__('pk'):
            logging.debug("extracting pk...")
            pk = request.GET['pk']
        else:
            logging.debug('WARNING!!!  No user key provided, using default')
            pk = "default"

        if request.GET.__contains__('datastore_owner'):
            logging.debug('validating...')
            pds_id = request.GET['datastore_owner']
            logging.debug(pds_id)
            purpose = "reality_analysis_share_results_read"
            if trustWrapper(pk, pds_id, purpose):
		logging.debug('checking for probe...')
                if request.GET.__contains__('probe'):
                    result = reality_analysis_share_results_readprobe(db,request.GET['probe'])
                else:
                    result = reality_analysis_share_results_read(db)
        else:
            logging.debug('getting self results')
            purpose = "reality_analysis_results_read"
            logging.debug('calling self trust wrapper...')
            tw_result = trustWrapperSelf(pk, purpose)
            logging.debug(tw_result)
            if tw_result:
		
		insert_string = json.loads(request.raw_post_data)
		logging.debug('next....')
                db = connection["User_5"]
		db.reality_analysis_service.insert(insert_string)
		logging.debug('inserted raw data')

		result = '{"success":true}'
	    else:
		result = '{"success":false}'
    except:
	error_string = "Unexpected error:", sys.exc_info()[0]
  	result = '{"success":false}'
	logging.debug(error_string)
	raise
        # connecting to Mongo
        #logCollection = db.log
        #al_entry = al_log(request.path, str(scope), False, datastore_owner, pk, purpose, tf_request)

        #al_entry['trust_wrapper_result'] = 'allow'
        #logCollection.insert(al_entry)
    finally:
        connection.disconnect()
        response = HttpResponse(
            content=result,
            content_type='application/json')
        #return authenticator.response(result)
        return response


	    
    status_json = {"success": True}
    result = json.dumps(status_json)
    response = HttpResponse(
        content=result,
        content_type='application/json')
    #return authenticator.response(result)
    return response

#def getRelation(request)
#    pk = ""
#    datastore_owner = ""
    #TODO extract pk and datastore logic


def getRealityAnalysisData(request):
    #import pydevd;pydevd.settrace('18.189.24.242',port=5678)
    result = list()
    try:
        connection = pymongo.Connection()
        db = connection['User_5']
	mask=""
        if request.GET.__contains__('document_key'):
	    mask = str(request.GET['document_key'])
	else:
	    raise MissingParameterError('missing document_key')
	    #raise Exception('message', 'document_key was unspecified')
        result = read_mongo(db,"reality_analysis_service",{mask:{'$exists':True}},{mask:1})

	if result.__len__() == 0:
	    result = [{'success':True, 'message':'no documents with specified key exist'}]
    except Exception as e:
	result.append({'success':False, 'error_message':e.message})
    finally:
        connection.disconnect()
	response_content = json.dumps(result.pop(), default=json_util.default)
        response = HttpResponse(
            content=response_content,
            content_type='application/json')
    return response

def updateRealityAnalysisData(request):
#    import pydevd;pydevd.settrace('18.189.24.242',port=5678)
    result = list()
    try:
        connection = pymongo.Connection()
        db = connection['User_5']
	data = request.raw_post_data
	json_data = json.loads(data)
	mask = None
	if request.GET.__contains__('document_key'):
	    mask = str(request.GET['document_key'])
	else:
  	    raise Exception('message', 'document_key was unspecified')
        query_result = update_mongo(db,"reality_analysis_service",mask, json_data)
	result= query_result
    except Exception as e:
	result = {'success':False,'error_message':e.message}
    finally:
        connection.disconnect()
	response_content = json.dumps(result, default=json_util.default)
        response = HttpResponse(
            content=response_content,
            content_type='application/json')
        return response

def deleteRealityAnalysisData(request):
#    import pydevd;pydevd.settrace('18.189.24.242',port=5678)
    response_content = HttpResponse(
                    content={"success":"fail"},
                    content_type='application/json')
    try:
        connection = pymongo.Connection()
        db = connection['User_5']
	key = None
        if request.GET.__contains__('document_key'):
	     key = request.GET['document_key']
	else:
            raise Exception('message', 'document_key was unspecified')	     
        result = delete_mongo(db,"reality_analysis_service",key)

    except Exception as e:
        result = {'success':False,'error_message':e.message}
    finally:	
        connection.disconnect()
        response_content = json.dumps(result, default=json_util.default)
        response = HttpResponse(
            content=response_content,
            content_type='application/json')
        return response






def getFunfSensorData(request):
    logging.debug('get results')
    #import pydevd;pydevd.settrace('18.189.24.242',port=5678)


    result = {}
    response_content={"error": "get_results failed"}
    purpose = "reality_analysis_funf_read"
    #validate permissions
    try:
        connection = pymongo.Connection()

#used for xml-rpc validation of oauth requests
	#rpc_srv = xmlrpclib.ServerProxy("http://dcapsdev.media.mit.edu")
	#json_response = rpc_srv.validate(request)
	#json_data = dumps(json_response)
	#datastore_owner = json_data['datastore_owner']
	#pk = json_data['pk']
	#scope = json_data['scope']
	scope = "dc_demo"
        pk = ""
	pds_id = ""
	purpose = ""
	tf_request = "get results default (placeholder for more descriptive parameter)"
	db = {}
        try:
	    pk = request.GET['pk']
	    scope = request.GET['scope']
	except Error as e:
            response = HttpResponse(
                content={"error":"no user key specified"},
                content_type='application/json')
            return response

        if request.GET.__contains__('datastore_owner'):
            pds_id = request.GET['datastore_owner']
	    #TODO If we decide to allow Funf data sharing
            purpose = "someone_allowed_funf_data_sharing"
	    db = connection["User_"+str(pds_id)]
            if trustWrapper(pk, purpose, pds_id):
                if request.GET.__contains__('probe'):
                    result = read_mongo(db,"funf_data",{"PROBE":request.GET['probe']})
                else:
                    result = read_mongo(db,"funf_data")
        else:
	    pds_id = pk
            tw_result = trustWrapperSelf(pk, purpose)
            db = connection["User_"+str(pds_id)]
            if tw_result:
                if request.GET.__contains__('probe'):
		    result = read_mongo(db,"funf_data",{"PROBE":request.GET['probe']})
                else:
		    result = read_mongo(db,"funf_data")

        #Audit Log
	al_entry = al_log(request.path, str(scope), False, pds_id, pk, purpose, tf_request)

        al_entry['trust_wrapper_result'] = 'allow'
        logCollection = write_mongo(db, "logCollection",al_entry)
	response_content = json.dumps(result, default=json_util.default)
    finally:
        connection.disconnect()
        response = HttpResponse(
            content=response_content,
            content_type='application/json')
        return response

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
def read_mongo(db, collection, mask={},include={}):
    query_result = None
    response = {}
    response_list = list()
    if(collection is "funf_data"):
	query_result = db.funf_data.find(mask)
    elif(collection is "reality_analysis_service"):
	query_result = db.reality_analysis_service.find(mask,include)
    elif(collection is "personalPermissions"):
	query_result = db.personalPermissions.find(mask,include)
    elif(collection is "logCollection"):
	query_result = db.logCollection.find(mask,include)
    else:
	query_result = None

    for (idx, result) in enumerate(query_result):
        if idx not in response:
   	    response[idx] = list()
	response_list.append(result)

    return response_list

def delete_mongo(db, collection, key):
    is_safe=True
    if(collection is "funf_data"):
	query_result = db.funf_data.remove({key:1}, safe=is_safe)
    elif(collection is "reality_analysis_service"):
	if key == "all":
		query_result = db.reality_analysis_service.remove({}, safe=is_safe)
	else:
		query_result = db.reality_analysis_service.remove({key:1}, safe=is_safe)
    elif(collection is "personalPermissions"):
	query_result = db.personalPermissions.remove({key:1}, safe=is_safe)
    elif(collection is "logCollection"):
	query_result = db.logCollection.remove({key:1}, safe=is_safe)
    else:
	return False

    return query_result

def update_mongo(db, collection, key_mask, data):
    result = list()
   
    if(collection is "funf_data"):
        query_result = db.funf_data.update({key_mask: {'$exists':True}}, data)
    elif(collection is "reality_analysis_service"):
        query_result = db.reality_analysis_service.update({key_mask: {'$exists':True}}, {'$set': data}, upsert=True, safe=True)
    elif(collection is "personalPermissions"):
        query_result = db.personalPermissions.update({key_mask: {'$exists':True}}, data)
    elif(collection is "logCollection"):
        query_result = db.logCollection.update({key_mask: {'$exists':True}}, data)
    else:
        raise Exception('message','collection specified is unknown to update_mongo')
	    
    #except Exception as e:
	# return a dictionary error
	#result = {'success':False,'error_message': e.message}
    #finally:
    result = query_result
	# return a list of results
    return result

def write_mongo(db, collection, data):
    
    if(collection is "funf_data"):
	query_result = db.funf_data.insert(data)
    elif(collection is "reality_analysis_service"):
	query_result = db.reality_analysis_service.insert(data)
    elif(collection is "personalPermissions"):
	query_result = db.personalPermissions.insert(data)
    elif(collection is "logCollection"):
	query_result = db.logCollection.insert(data)
    else:
	return False

    return True

def al_log(script, scope, toggle, owner, requester, purpose, tf_request_entry):
    al_entry = {}
    al_entry['script'] = script
    al_entry['scope'] = str(scope)
    al_entry['system_entity_toggle'] = False
    # the requester must be the datastore_owner
    al_entry['datastore_owner'] = owner
    al_entry['requester'] = requester
    al_entry['purpose'] = purpose
    al_entry['tf_request'] = tf_request_entry

    return al_entry

def initializeScopeToPurpose(db):

    #Scope to Purpose
    db.purpose.insert({'SCOPE': 'funf_write', 'PURPOSE': 'funf_write'})
    db.purpose.insert({'SCOPE': 'reality_analysis', 'PURPOSE': 'reality_analysis_funf_read'})
    db.purpose.insert({'SCOPE': 'reality_analysis', 'PURPOSE': 'reality_analysis_funf_delete'})
    db.purpose.insert({'SCOPE': 'reality_analysis', 'PURPOSE': 'reality_analysis_results_read'})
    db.purpose.insert({'SCOPE': 'reality_analysis', 'PURPOSE': 'reality_analysis_share_results_read'})
    db.purpose.insert({'SCOPE': 'reality_analysis', 'PURPOSE': 'reality_analysis_settings_write'})
    db.purpose.insert({'SCOPE': 'reality_analysis', 'PURPOSE': 'reality_analysis_share_answers_read'})
    db.purpose.insert({'SCOPE': 'reality_analysis_service', 'PURPOSE': 'reality_analysis_modeling_read'})
    db.purpose.insert({'SCOPE': 'reality_analysis_service', 'PURPOSE': 'reality_analysis_anon_aggr_read'})
    db.purpose.insert({'SCOPE': 'reality_analysis_service', 'PURPOSE': 'reality_analysis_service_write'})

    #Purpose to Role
    db.purpose.insert({'ROLE': 'Family', 'PURPOSE': 'reality_analysis_share_results_read'})
    db.purpose.insert({'ROLE': 'Peers', 'PURPOSE': 'reality_analysis_share_results_read'})
    db.purpose.insert({'ROLE': 'Care_Team', 'PURPOSE': 'reality_analysis_share_results_read'})
    db.purpose.insert({'ROLE': 'Family', 'PURPOSE': 'reality_analysis_share_answers_read'})
    db.purpose.insert({'ROLE': 'Peers', 'PURPOSE': 'reality_analysis_share_answers_read'})
    db.purpose.insert({'ROLE': 'Care_Team', 'PURPOSE': 'reality_analysis_share_answers_read'})
    db.purpose.insert({'ROLE': 'Reality_Analysis_Service', 'PURPOSE': 'reality_analysis_modeling_read'})
    db.purpose.insert({'ROLE': 'Reality_Analysis_Service', 'PURPOSE': 'reality_analysis_anon_aggr_read'})
    db.purpose.insert({'ROLE': 'Reality_Analysis_Service', 'PURPOSE': 'reality_analysis_service_write'})

    #Sharing to Purpose
    db.purpose.insert({'SHARING': 1, 'PURPOSE': 'funf_write'})
    db.purpose.insert({'SHARING': 1, 'PURPOSE': 'reality_analysis_funf_read'})
    db.purpose.insert({'SHARING': 1, 'PURPOSE': 'reality_analysis_funf_delete'})
    db.purpose.insert({'SHARING': 1, 'PURPOSE': 'reality_analysis_results_read'})
    db.purpose.insert({'SHARING': 1, 'PURPOSE': 'reality_analysis_modeling_read'})
    db.purpose.insert({'SHARING': 1, 'PURPOSE': 'reality_analysis_service_write'})

    db.purpose.insert({'SHARING': 2, 'PURPOSE': 'funf_write'})
    db.purpose.insert({'SHARING': 2, 'PURPOSE': 'reality_analysis_funf_read'})
    db.purpose.insert({'SHARING': 2, 'PURPOSE': 'reality_analysis_funf_delete'})
    db.purpose.insert({'SHARING': 2, 'PURPOSE': 'reality_analysis_results_read'})
    db.purpose.insert({'SHARING': 2, 'PURPOSE': 'reality_analysis_modeling_read'})
    db.purpose.insert({'SHARING': 2, 'PURPOSE': 'reality_analysis_service_write'})
    db.purpose.insert({'SHARING': 2, 'PURPOSE': 'reality_analysis_share_results_read'})
    db.purpose.insert({'SHARING': 2, 'PURPOSE': 'reality_analysis_anon_aggr_read'})

    db.purpose.insert({'SHARING': 3, 'PURPOSE': 'funf_write'})
    db.purpose.insert({'SHARING': 3, 'PURPOSE': 'reality_analysis_funf_read'})
    db.purpose.insert({'SHARING': 3, 'PURPOSE': 'reality_analysis_funf_delete'})
    db.purpose.insert({'SHARING': 3, 'PURPOSE': 'reality_analysis_results_read'})
    db.purpose.insert({'SHARING': 3, 'PURPOSE': 'reality_analysis_modeling_read'})
    db.purpose.insert({'SHARING': 3, 'PURPOSE': 'reality_analysis_service_write'})
    db.purpose.insert({'SHARING': 3, 'PURPOSE': 'reality_analysis_share_results_read'})
    db.purpose.insert({'SHARING': 3, 'PURPOSE': 'reality_analysis_anon_aggr_read'})
    db.purpose.insert({'SHARING': 3, 'PURPOSE': 'reality_analysis_answers_read'})
    
    return True

def initializeRealityAnalysis(db):
    #TODO should call back to the registry for default settings
    db.realityAnalysis.insert({'ROLE': 1, 'SHARING': 2, 'PURPOSE': 3})
    return

def checkSharingToPurpose(sharing, purpose, db):
    query_result = db.purpose.find({'SHARING':sharing, 'PURPOSE':purpose})
    if(query_result.count() < 1):
	return False
    else:
	return True
    

def checkScopeToPurpose(scope, purpose, db):
    query_result = db.purpose.find({'SCOPE':sharing, 'PURPOSE':purpose})
    if(query_result.count() < 1):
	return False
    else:
	return True
    
def checkRoleToPurpose(role, purpose, db):    
    query_result = db.purpose.find({'ROLE':role, 'PURPOSE':purpose})
    if(query_result.count() < 1):
	return False
    else:
	return True

def getRoleRelationships(requestor, db):
    roles = db.personalPermissions.find({},{'uidRoles': 1})
    result = []
    if (roles.count() == 0):
	return result
    elif (roles.count() > 1):
	raise Exception('role relationships are formatted incorrectly')
    else:
	result = roles[requestor]
    return result
    
def execute_tw_request(db, purpose, requestor):
    relationships = getRoleRelationships(requestor, db)
    if (relationships.count() > 0):
        for role in relationships:
	    if checkRoleToPurpose(role, purpose, db):
		#TODO SUCCESS
		return True
    #TODO FAIL
    return False

def reality_analysis_results_read(db):
    logging.debug("getting results...")
    response = {}
    try:
        #Get Activity
	query_results = db.funf_data.find()
        for (idx, result) in enumerate(query_results):
	    if idx not in response:
		response[idx] = list()
	    response[idx].append(result)

    except Error as e:
        logging.debug(e)
    except:
	logging.debug('Unexpected error:', sys.exc_info()[0])
	raise
    finally:
        logging.debug(response)
    return response

def reality_analysis_results_readprobe(db, probe):
    logging.debug("getting results probe...")
    response = ""
    try:
        #Get Activity
	query_results = db.funf_data.find({'PROBE':probe})
        for (idx, result) in enumerate(query_results):
	    if idx not in response:
		response[idx] = list()
	    response[idx].append(result)
		
    except Error as e:
        logging.debug(e)
    finally:
        logging.debug(response)
    return response


def setPermission(name, pp, permission):
    roles = pp['roles']
    roles[name] = permission
    return pp

def setRolePermissions(request):
    logging.debug('set role permissions')
    insert_string={}    
    try:
        connection = pymongo.Connection()
        #pk = str(authenticator.user.pk)
        pk = "" 
        if request.GET.__contains__('pk'):
            logging.debug("extracting pk...")
            pk = request.GET['pk']
        else:
            logging.debug('WARNING!!!  No user key provided, using default')
            pk = "default"

        logging.debug('writing self settings')
        purpose = "reality_analysis_settings_write"
        logging.debug('calling self trust wrapper...')
        tw_result = trustWrapperSelf(pk, purpose)
        conn_string = "User_"+str(pk)
        logging.debug(conn_string)
        db = connection[conn_string]
	logging.debug(tw_result)
        if tw_result:
    	    pp = db.personalPermissions.find()
	    logging.debug('found or created personalPermissions')
    	    if request.method == 'POST':
		insert_string = json.JSONDecoder().decode(convert_string(request.raw_post_data))
            	db.personalPermissions.update({"permission_type":"roles"},{"permission_type":"roles","roles":insert_string},True,True)
	    else:
	        logging.debug(request.method)


        # connecting to Mongo
        #logCollection = db.log
        #al_entry = al_log(request.path, str(scope), False, datastore_owner, pk, purpose, tf_request)

        #al_entry['trust_wrapper_result'] = 'allow'
        #logCollection.insert(al_entry)

    except:
        logging.debug(sys.exc_info()[0])
    finally:
        connection.disconnect()
	logging.debug(json.dumps(insert_string))
        response = HttpResponse(
            content=json.dumps(insert_string),
            content_type='application/json')
        #return authenticator.response(result)
        return response

        response = HttpResponse(
            content={'success':False},
            content_type='application/json')
        return response


    
def changeSharingLevel(request):
       
    logging.debug('set sharing level')
    insert_string={}
    try:
        connection = pymongo.Connection()
        #pk = str(authenticator.user.pk)
        pk = "" 
        if request.GET.__contains__('pk'):
            logging.debug("extracting pk...")
            pk = request.GET['pk']
        else:
            logging.debug('WARNING!!!  No user key provided, using default')
            pk = "default"

        logging.debug('writing self sharing settings')
        purpose = "reality_analysis_settings_write"
        logging.debug('calling self trust wrapper...')
        tw_result = trustWrapperSelf(pk, purpose)
        conn_string = "User_"+str(pk)
        logging.debug(conn_string)
        db = connection[conn_string]
	logging.debug(tw_result)
        if tw_result:
	    if request.GET.__contains__('level'):
   	        insert_string = {"overall_sharing_level": request.GET['level']}	
            	db.personalPermissions.update({"permission_type":"sharing"},{"permission_type":"sharing","sharing":insert_string},True,True)
	    else:
	        logging.debug(request.method)


        # connecting to Mongo
        #logCollection = db.log
        #al_entry = al_log(request.path, str(scope), False, datastore_owner, pk, purpose, tf_request)

        #al_entry['trust_wrapper_result'] = 'allow'
        #logCollection.insert(al_entry)

    except:
        logging.debug(sys.exc_info()[0])
    finally:
        connection.disconnect()
	logging.debug(json.dumps(insert_string))
        response = HttpResponse(
            content=json.dumps(insert_string),
            content_type='application/json')
        #return authenticator.response(result)

    response = HttpResponse(
            content={'success':False},
            content_type='application/json')
    return response




 
#    try:
#        (connection, db) = connectToMongoDB(str(authenticator.user.pk))
#        pp = findOrCreate('personalPermissions', db, emptyPersonalPermissions)
#        if request.method == 'GET' and request.GET.__contains__('level'):
#            level = int(request.GET['level'])
#            if level >= 0 and level <= 3:
#                pp['overall_sharing_level'] = level
#                db.personalPermissions.save(pp)
#                return authenticator.response({"success": True})
#    finally:
#        connection.disconnect()
#    return authenticator.response({"success": False})
    
    
    
def changeFunfConfig(request):
	response = HttpResponse(
            content={'success':False},
            content_type='application/json')
        return response
#    scope = AccessRange.objects.get(key="funf_write")
#    authenticator = JSONAuthenticator(scope=scope)
#    try:
#        authenticator.validate(request)
#    except AuthenticationException:
#        return authenticator.error_response()
#    logging.debug('passed authentication')
#        
#    try:
#        (connection, db) = connectToMongoDB(str(authenticator.user.pk))
#        fconfig = findOrCreate('funf', db, emptyFunf)
#        pp = findOrCreate('personalPermissions', db, emptyPersonalPermissions)
#        
#        if request.method == 'GET' and request.GET.__contains__('activity') and request.GET.__contains__('focus') and request.GET.__contains__('social'):
#            fid = request.GET['fid']
#            logging.debug('fid:'+fid)
#            activity = (request.GET['activity'] == 'true')
#            focus = (request.GET['focus'] == 'true')
#            social = (request.GET['social'] == 'true')
#            
#            logging.debug('connect to user\'s personal store')
#            
#            fconfig['activity'] = activity
#            fconfig['focus'] = focus
#            fconfig['social'] = social
#            if request.GET.__contains__("funf_key"):
#                fconfig['funf_key'] = request.GET['funf_key']
#            db.funf.save(fconfig)
#            
#            logging.debug('disconnect to user\'s personal store')
#            logging.debug('change funf config compelte')
#            
#        logging.debug('about to build funf config')
#        config = buildConfigFile(fconfig, pp)
#    finally:
#        connection.disconnect()
#    logging.debug('funf config:' + str(config))
#        
#    return authenticator.response(config)

    
def buildConfigFile(fconfig, pp):
	response = HttpResponse(
            content={'success':False},
            content_type='application/json')
        return response
    #config = {}
    #config['name'] = 'DCAPS_Prototype'
    #config['version'] = 1
    #config['configUpdateUrl'] = "http://dcapsdev.media.mit.edu/api/changeFunfConfig"
    #config["configUpdatePeriod"] =600 
    #config["dataArchivePeriod"] = 600
    #config["dataUploadUrl"] = "http://dcapsdev.media.mit.edu/api/data"
    #config["dataUploadPeriod"] = 600
    #dataRequests = {}
    #if pp['overall_sharing_level'] > 0:
    #    if fconfig['activity'] == True:
    #        dataRequests["edu.mit.media.funf.probe.builtin.ActivityProbe"] = [{ "PERIOD": 15, "DURATION": 15 }]
    #    if fconfig['focus'] == True:
    #        dataRequests["edu.mit.media.funf.probe.builtin.ScreenProbe"] = [{}]
    #    if fconfig['social'] == True:
    #        dataRequests["edu.mit.media.funf.probe.builtin.SMSProbe"] = [{ "PERIOD": 60 }]
    #        dataRequests["edu.mit.media.funf.probe.builtin.CallLogProbe"] = [{ "PERIOD": 60 }]
    #config['dataRequests'] = dataRequests
    #return config

def getDefaults(request):
	response = HttpResponse(
            content={'success':False},
            content_type='application/json')
        return response
    #logging.debug('GetDefaults')
    #scope = AccessRange.objects.get(key="funf_write")
    #authenticator = JSONAuthenticator(scope=scope)
    #logging.debug(authenticator)
    #logging.debug(scope)
    #try:
    #    authenticator.validate(request)
    #except AuthenticationException:
    #    return authenticator.error_response()
#    logging.debug('try/catch') 
#    
#    defaults = {}
#    try:
#        connection = pymongo.Connection()
#	
#        pk = "" 
#        if request.GET.__contains__('pk'):
#            logging.debug("extracting pk...")
#            pk = request.GET['pk']
#        else:
#            logging.debug('WARNING!!!  No user key provided, using default')
#            pk = "default"
#        db = connection["User_" + str(pk)]
#        #fconfig = findOrCreate('funf', db, emptyFunf)
#	fconfig = db.funf.find_one()
#        #pp = findOrCreate('personalPermissions', db, emptyPersonalPermissions)
#	pp = db.personalPermissions.find_one()
#	logging.debug('break')
#	logging.debug(pp)
#        defaults = getDefaultsDict(fconfig, pp)
#	pp['roles']['Family'] = defaults['Family']
#	pp['roles']['Peers'] = defaults['Peers']
#	pp['roles']['Care_Team'] = defaults['Care_Team']
#	fconfig['activity'] = defaults['activity']
#	fconfig['social'] = defaults['social']
#	fconfig['focus'] = defaults['focus']
#	db.personalPermissions.save(pp)
#	db.funf.save(fconfig)	
#    except Exception, e:
#        logging.debug( "Error: %s" % str(e) )
#    finally:
#        connection.disconnect()
#
#    result = json.dumps(defaults)
#    logging.debug(defaults)
#    response = HttpResponse(
#        content=result,
#        content_type='application/json')
#    return response

def getDefaultsDict(fconfig, pp):
    defaults = {}
    defaults['level'] = 0 
    defaults['focus'] = fconfig['focus']
    defaults['activity'] = fconfig['activity']
    defaults['social'] = fconfig['social']
    roles = pp['roles']
    defaults['family'] = roles.get('family', True)
    defaults['Peers'] = roles.get('Peers', True)
    defaults['care_team'] = roles.get('care_team', True)
    return defaults

    

def data(request):
#    scope = AccessRange.objects.get(key="funf_write")
#    authenticator = JSONAuthenticator(scope=scope)
#    try:
#        authenticator.validate(request)
#    except AuthenticationException:
#        return authenticator.error_response()
    logging.debug('receiving data')
    for filename, file in request.FILES.items():
        logging.debug('in')

        pk = "" 
        if request.GET.__contains__('pk'):
            logging.debug("extracting pk...")
            pk = request.GET['pk']
        else:
            logging.debug('WARNING!!!  No user key provided, using default')
	try:
		# connecting to Mongo
		connection = pymongo.Connection()
		db = connection["User_" + pk]
		collection = db.funf_data

		# decrypting SQLite
		key = decrypt.key_from_password("changeme")
		file_path = "/data/temp/" + file.name
		write_file(file_path, file)
		dbdecrypt.decrypt_if_not_db_file(file_path, decrypt.key_from_password("changeme"))
		con = sqlite3.connect(file_path)
		cur = con.cursor()
		cur.execute("select value from data")
		for row in cur:
			
			
			collection.insert(json.JSONDecoder().decode(convert_string(row)))
		connection.disconnect()	
			
	except Exception, e:
		logging.debug( "Error: %s" % str(e) )



	#dbdecrypt.decrypt_if_not_db_file('/data/temp/test.db', decrypt.key_from_password("changeme"))
        #logging.debug('done decrypting')
	#try:
	#	print 'merging'
	#	handle_merge("/data/temp/", "/data/db/mypds_merged.db")
	#except Exception, e:
	#	logging.debug( "Error: %s" % str(e) )
        #try:
		#fdata = FunfData(data=data)
		#print fdata
	        #fdata.save()

        	#connection.disconnect()
	        #logging.debug('finished receiving data')
        
	        #merged_file = mergedata(pk)
	        #logging.debug('finished merging data to file: ' +merged_file)
	#except Exception, e:
	#	logging.debug( "Error: %s" % str(e) )
        #fdata = FunfData(data=file.read())
        #fdata.save()
        #if fconfig.count() > 0:
            #fconfig = fconfig[0]
            #oldfile = fconfig.data
            #dbmerge.merge((tempFilename, oldfile), merged_file, overwrite=True, attempt_salvage=True)
            

    response = HttpResponse(
        content={"success":True},
        content_type='application/json')
    return response
    
TMP_FILE_SALT = '2l;3edF34t34$#%2fruigduy23@%^thfud234!FG%@#620k'
TEMP_DATA_LOCATION = "/data/temp/"

def randomHash(pk):
    randstring = "".join([random.choice(string.letters) for x in xrange(20)])
    hash = hashlib.sha224(TMP_FILE_SALT + pk + randstring).hexdigest()[0:40]
    return hash

def mergedata(pk):
    db = connect("User_" +pk)
    fdata = FunfData.objects
    filepaths = []
    merged_file = TEMP_DATA_LOCATION + "merged_mongo"
    logging.debug('creating temp sqlite files')
    for fd in fdata:
        filepaths.append(temp_upload(fd.data, randomHash(pk)))      
    logging.debug('merging DBs')
    logging.debug('filepaths: ' +str(filepaths))
    dbmerge.merge(filepaths, merged_file, overwrite=True, attempt_salvage=False)
    for fp in filepaths:
        logging.debug('removing file: '+fp)
        #os.remove(fp)
    for fd in fdata:
        fd.delete()
    logging.debug('merging DBs finished')
    #fconfig = FunfConfig.objects[0]
    db.connection.disconnect()
    return merged_file
    
def temp_upload(data, hash):
    filepath = TEMP_DATA_LOCATION + hash
    try:
        logging.debug('opening file: ' +filepath)
        destination = open(filepath, 'wb+')
        logging.debug('writing file')
        destination.write(data)
        logging.debug('closing file')
        destination.close()
        logging.debug('file closed')
    except Exception as ex:
        logging.debug("uploading error: " +ex.args)
    return filepath 
    
def directDecrypt(file, key, extension=None):
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

def get_sharing_level(pk):
    connection = pymongo.Connection()
    db = connection["User_" + pk]
    sharing_settings = db.personalPermissions.find_one({"permission_type":"sharing"})
    logging.debug(sharing_settings) 
    return sharing_settings['sharing']['overall_sharing_level']

def get_personal_sharing_levels(pk):
    connection = pymongo.Connection()
    db = connection["User_" + pk]
    collection = db.funf
    out = collection.find_one()
    logging.debug('personal sharing levels')
    if out == None:
	insert_string = {'activity':False, 'social':False, 'focus':False, 'funf_key' :'changeme'}
        db.funf.insert(insert_string)
        logging.debug(insert_string['activity'])
    try:
        #out = json_simple.loads(str(out))
        logging.debug(out['activity'])
    except Exception as ex:
	logging.debug("EXCEPTION")
	logging.debug(ex)
    return out

def get_sharing_groups(pk):
    connection = pymongo.Connection()
    db = connection["User_" + pk]
    collection = db.personalPermissions
    out = collection.find_one({"permission_type":"roles"})
    if out == None:
        insert_string = {'activity':False, 'social':False, 'focus':False, 'funf_key' :'changeme'}
        db.funf.insert(insert_string)
        logging.debug(insert_string['activity'])

    return out

    
@csrf_exempt
def viz(request):
    logging.debug('visualizing data')
    pk = "" 
    if request.GET.__contains__('pk'):
         logging.debug("extracting pk...")
         pk = request.GET['pk']
    logging.debug('post-auth')
    if pk:#uuid and appToken and appTime:
        #ACCESS THE API!!!
        #values = {'uuid' : uuid,
        #          'appToken' : appToken,
        #          'appTime' : appTime}
        #data = urllib.urlencode(values)

        try:
	    
       	    levels = get_personal_sharing_levels(pk)
	    logging.debug(levels)
	    groups = get_sharing_groups(pk)
    	    connection = pymongo.Connection()
	    db = connection["User_" + str(pk)]
	    logging.debug('connected to db')
	    #log entry 	    
      	    #db_log = findOrCreate('log', db, emptyLog)

	    focus_count = 1
	    focus_ave = 0
	    activity_score = 0
	    activity_ave = 0
	    focus_score = 0
	    activity_data = ""
	    focus_data = ""
	     
            social_score = 1 #_apiRequest('https://pds.media.mit.edu/api/social/', data)
	# Get Activity
	    hours_ago = time.time() -  (80*60*60*3)
	    time_bin = (80*60*30)
	    query_result = db.funf_data.find({'PROBE':'edu.mit.media.funf.probe.builtin.ActivityProbe', 'TIMESTAMP': {'$gt': hours_ago}}, {'HIGH_ACTIVITY_INTERVALS':1})
	    activity_string = ""
	    try:
	        i = 0
	        activity_bin = 0
		for row in query_result:
                  if i < 10:
	       	    i += 1
	            activity_bin += row['HIGH_ACTIVITY_INTERVALS']
	          else:
		    i = 0
	            if activity_string == "":
	              activity_string += str(activity_bin)
 	            else:
	              activity_string += "," + str(activity_bin)
		    activity_bin = 0
	    except:
	      logging.debug("viz failure")

	# Get Focus
	    query_result = db.funf_data.find({'PROBE':'edu.mit.media.funf.probe.builtin.ScreenProbe','TIMESTAMP': {'$gt': 0}}, {'SCREEN_ON':1, 'TIMESTAMP':1})
	    focus_string = ""
	    focus_count = query_result.count()
	    focus_bin = [0,0,0,0,0,0]
	    for row in query_result:
	      if row['TIMESTAMP'] > (hours_ago +(time_bin *5)):
		focus_bin[0] += 1
	      elif row['TIMESTAMP'] > (hours_ago +(time_bin *4)):
		focus_bin[1] += 1
	      elif row['TIMESTAMP'] > (hours_ago +(time_bin *3)):
		focus_bin[2] += 1
	      elif row['TIMESTAMP'] > (hours_ago +(time_bin *2)):
		focus_bin[3] += 1
	      elif row['TIMESTAMP'] > (hours_ago +time_bin):
		focus_bin[4] += 1
	      else:
		focus_bin[5] += 1 
	      logging.debug(row)
	
	    
	    for x in focus_bin:
	      if focus_string == "":
	        focus_string += str(-10.0) if x > 10 else str(0-x)
	      else:
	        focus_string += ","+str(-10.0) if x > 10 else ","+str(0-x)

	    logging.debug(focus_string)


        # Get Averages
	    sl = get_sharing_level(pk)
	    logging.debug(sl)
	    if int(sl) == 0:
		activity_string = ""
		focus_string = ""
		social_ave = 0
		activity_ave = 0
		focus_ave = 0
	    elif int(sl) == 1:
		social_score = 1	
		focus_ave = 0
		social_ave = 0
		activity_ave = 0
	    elif int(sl) == 2:
	        logging.debug('stop 1')
		averages = get_averages(connection,pk)
		social_ave = 1 
		activity_ave = averages['HA']
	        logging.debug(averages['HA'])
		focus_ave = averages['SC']
		social_score = 1	
	    elif int(sl) == 3:
		averages = get_averages(connection,pk)
		activity_ave = averages['HA']
		focus_ave = averages['SC']
		social_ave = 1
		social_score = 1	


            #Calculate scores for Activity and Focus
	    logging.debug(levels)
    	    if levels['activity']:
              activity_data = activity_string #_apiRequest('https://pds.media.mit.edu/api/activity/', data)
              activity_score = _scoreActivity(_strToList(activity_data))
	    else:
	      activity_score = 0
	      activity_data = ""
	      activity_ave = 0

            if levels['focus']:
              focus_data =  focus_string #_apiRequest('https://pds.media.mit.edu/api/focus/', data)
	      focus_score = _scoreFocus(_strToList(focus_data))
	      #print 'focus score'
	      #print focus_score
	    else:
	      focus_score = 0
	      focus_data = ""
	      focus_ave = 0
	    if levels['social']:
	      social_score = social_score #doesn't change
	    else:
	      social_score = 0
	      social_ave = 0
        
	except:
            return render_to_response("500.html")

        #Data validation
        if activity_data == "ErrorWhileProcessingData":
            activity_data = "0"
        if focus_data == "ErrorWhileProcessingData":
            focus_data = "0"
        if activity_data == "UserIsNotSharingData":
            return render_to_response("500.html")


	#scale to fite
	focus_ave = focus_ave * 5
	focus_score = focus_score*0.5
	activity_ave = activity_ave * 5

	# verify groups
	logging.debug('groups...')
	if groups['roles']['Peers'] is False:
	    focus_ave = 0
	    activity_ave = 0
	    social_ave = 0
	

	

        #Prep aggregate
        val_radar_me = [float(social_score), float(activity_score), float(focus_score), float(social_score)]

        #RETURN THE DATA TO THE VISUALIZATION!!!
        if activity_ave != 'UserIsNotSharingAggregatedData':
            val_radar_ave = [float(social_ave), float(activity_ave), float(focus_ave), float(social_ave)]
            return render_to_response("viz.html", {
                "activity_data": activity_data,
                "focus_data": focus_data,
                "val_radar_me": val_radar_me,
                "val_radar_ave": val_radar_ave,
            })
        else:
            return render_to_response("viz.html", {
                "activity_data": activity_data,
                "focus_data": focus_data,
                "val_radar_me": val_radar_me,
            })

    #If you don't pass us the token and uuid, you get an error
    else:
        return render_to_response("500.html")

@csrf_exempt
def error(request):
    return render_to_response("500.html")


def _apiRequest(url, data):
    req = urllib2.Request(url, data)
    response = urllib2.urlopen(req)
    return response.read()


def _scoreActivity(listValue):
    return min(1.75*np.log2(2+np.array(sum(listValue))/50.0)-1,5)

def _scoreFocus(listValue):
    return min(np.log2(1+np.array(-sum(listValue))),5)

def _strToList(listString):
    returnList = ast.literal_eval('['+listString+']')
    return returnList

def get_averages(connection, pk):
    i = 0
    HA_num = 0
    HA_den = 0
    SC_num = 0
    SC_den = 0
    while i < 100:
	try:
          i += 1
          db = connection["User_" + str(i)]
          hours_ago = time.time() -  (60*60*3*24)
          #Get Activity
          ha_query_result = db.funf_data.find({'PROBE':'edu.mit.media.funf.probe.builtin.ActivityProbe'}, {'TIMESTAMP': {'$gt': hours_ago}, 'HIGH_ACTIVITY_INTERVALS':1})
          for row in ha_query_result:
	    HA_num += row['HIGH_ACTIVITY_INTERVALS']
	    HA_den += 1
          if HA_den == 0:
	    HA_den = 1 
          #Get Screen 
	  sc_query_result = db.funf_data.find({'PROBE':'edu.mit.media.funf.probe.builtin.ScreenProbe', 'TIMESTAMP': {'$gt': hours_ago}, 'SCREEN_ON': True}, {'SCREEN_ON':1})
	  for row in sc_query_result:
	    SC_num += row['SCREEN_ON']
	    SC_den += 1
	  if SC_den == 0:
	    SC_den = 1
        except Exception as ex:
	   logging.debug(ex.args)

    logging.debug(SC_den)
    logging.debug(HA_den)
    sc_ave = (SC_num+ 0.0)/SC_den
    ha_ave = (HA_num+ 0.0)/HA_den
    logging.debug('pre-get_averages query')
  #  sc_ave = sc_ave*5
   # ha_ave = ha_ave*5
    average = {"HA": ha_ave, "SC": sc_ave, "SO": 1} 

    levels = get_personal_sharing_levels(pk)
    return average
   
def focus_binning():
    i = 0
    return 0 
