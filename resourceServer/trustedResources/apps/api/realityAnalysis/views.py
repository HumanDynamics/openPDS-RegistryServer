#-*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
import urllib
import urllib2
import hashlib
import datetime
import numpy as np
from oauthManagement.apps.api.mongoencoder import MongoEncoder
from oauth2app.authenticate import JSONAuthenticator, AuthenticationException
from django.http import HttpResponse
from oauth2app.models import AccessRange
from apps.account.models import *
#from account.models import *
from mongoengine import *
from datastoreModels import *
from django.utils import simplejson as simple_json
import logging, random, hashlib, string
#from decrypt import directDecrypt
import dbmerge, os
from oauthManagement.datastoreUtils import *
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

upload_dir = '/data/temp'

num_datastores = 100


def id_to_sid(guest, host_symbolic):
    #implement retrieval of id from symbolic id
    prof = Profile.objects.filter(user=guest)
    logging.debug('symbolic id to ID')
    logging.debug(prof)
    logging.debug(host_symbolic)
    mapping = UserToUser.objects.filter(profileGuest=prof[0], id=host_symbolic)
    if(mapping.count() != 1):
	logging.debug("couldn't find symbolic mapping.")
	return {"error": "counldn't find specified symbolic mapping"}
    logging.debug(mapping[0].profileHost)
    return mapping[0].profileHost

def sid_to_id(symbolic_id):
    logging.debug('ID to symbolic id')
    #implement retrieval of id from symbolic id
    actual_id = 0
    return actual_id

def setRealityAnalysisData(request):
    logging.debug('set reality analysis data')
    logging.debug(request.raw_post_data)
    return true

def getResults(request):
    logging.debug('get results')

    #validate REST
    #scope = AccessRange.objects.get(key="reality_analysis_service")
    #authenticator = JSONAuthenticator(scope=scope)

    #try:
    #    authenticator.validate(request)
    #except AuthenticationException:
    #    logging.debug(authenticator.error_response())
    #    return authenticator.error_response()

    result = ""
    #validate permissions
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

        logging.debug('getting results')
        if request.GET.__contains__('datastore_owner'):
            logging.debug('validating...')
            pds_id = request.GET['datastore_owner']
            logging.debug(pds_id)
            purpose = "reality_analysis_share_results_read"
            if trustWrapper(pk, pds_id, purpose):
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
            db = connection["User_" + pk]
            if tw_result:
                if request.GET.__contains__('probe'):
                    logging.debug('calling readprobe')
                    logging.debug(request.GET['probe'])
                    result = reality_analysis_results_readprobe(db,request.GET['probe'])
                else:
                    result = reality_analysis_results_read(db)


        # connecting to Mongo
        #logCollection = db.log
        #al_entry = al_log(request.path, str(scope), False, datastore_owner, pk, purpose, tf_request)

        al_entry['trust_wrapper_result'] = 'allow'
        logCollection.insert(al_entry)
    finally:
        connection.disconnect()
        logging.debug(result)
        response = HttpResponse(
            content=result,
            content_type='application/json')
        #return authenticator.response(result)
        return response

    return authenticator.response({ "success": False})



def trustWrapperSelf(pk, purpose):
    logging.debug('checking against self Trust Wrapper')
    try:
        connection = pymongo.Connection()
        db = connection["User_" + pk]
	logging.debug("wrapping")
        permissions = db.personalPermissions.find_one()
	#log request
        return True
    except TypeError as e:
	logging.debug('error...')
        logging.debug(e)
    finally:
	logging.debug('disconnecting...')
        connection.disconnect()
    return False

def trustWrapper(pk,pds_sid, purpose):
    logging.debug('checking against Trust Wrapper')
    try:
        #pds_id = sid_to_id(pds_sid)
        host = id_to_sid(pk, pds_sid)
	logging.debug("returned from id mapper")
        connection = pymongo.Connection()
	logging.debug("made connection")
        db = connection["User_" + str(host.user.id)]
	logging.debug("wrapping")
        permissions = db.personalPermissions.find_one()
        sharing_level = permissions['overall_sharing_level']
        permitted_roles = permissions['uidRoles'][requester_sid]
        db_RA = connection["RealityAnalysis"]

        for role in permitted_roles:
            if (db_RA.mapping.count({"ROLE":role, "LEVEL": sharing_level, "PURPOSE": purpose}) > 0):
                return True
    except TypeError as e:
	logging.debug('error...')
        logging.debug(e)
    finally:
	logging.debug('disconnecting...')
        connection.disconnect()
    return False

def setPermission(name, pp, permission):
    roles = pp['roles']
    roles[name] = permission
    return roles

def logRolePermissions(db,pp):
    #log entry 	    
    collection = db.log
    collection.insert({"test": "permission change log"})
    return True

def setRolePermissions(request):
    logging.debug('set role permissions')
    
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
	db = connection["User_" + datastore_owner]
	ra_db = connection["Reality_Analysis"]
        logCollection = db.log
        if request.GET.__contains__('purpose'):
    	    purpose = request.GET['purpose']
	    if purpose == 'reality_analysis_settings_write':
	        #success
		al_entry = {}
		al_entry['script'] = 'set_role_permissions'
		al_entry['scope'] = str(scope)
		al_entry['system_entity_toggle'] = False
		# the requester must be the datastore_owner
		al_entry['datastore_owner'] = datastore_owner 
		al_entry['requester'] = pk 
		al_entry['purpose'] = purpose
		al_entry['trust_wrapper_result'] = 'allow'	
                if request.GET.__contains__('family'):
                    al_entry['family'] = (request.GET['family'] == 'true')
                if request.GET.__contains__('peers'):
                    al_entry['peers'] = (request.GET['peers'] == 'true')
                if request.GET.__contains__('care_team'):
                    al_entry['care_team'] = (request.GET['care_team'] == 'true')
		logCollection.insert(al_entry)
	    else:
	       	logging.debug('invalid purpose')
	       	#handle invlaid purpose
	        authenticator.response({ "success": False})
	else:
	   logging.debug('missing purpose')
    finally:
        connection.disconnect()
        return authenticator.response({
            "success":True})
    # log REST success!
    # log TF success!
    return authenticator.response({ "success": False})

def al_log(script, scope, toggle, owner, requester, purpose, tf_reqest_entry):
    al_entry = {}
    al_entry['script'] = request.path
    al_entry['scope'] = str(scope)
    al_entry['system_entity_toggle'] = False
    # the requester must be the datastore_owner
    al_entry['datastore_owner'] = datastore_owner 
    al_entry['requester'] = pk 
    al_entry['purpose'] = purpose
    al_entry['tf_request'] = tf_req_entry

    return al_entry

def execute_tw_request(db, ra_db, purpose, requester):
    purpose
    ra_roles = ra_db.roles.find({"purpose": purpose}, {"roles":1})
    roles = db.personalPermissions.find({} ,{'uidRoles': 1})
    #if roles contains ra_roles
    # get the roles for the requester
    roles[requester]
    return True

#purposes

def reality_analysis_share_results_read(pk,pds_sid):
    total = ""
    try:
	pds_id = sid_to_id(pds_sid)
	requester_sid = id_to_sid(pk)
        connection = pymongo.Connection()
        db = connection["User_" + pds_id]
	permissions = db.personalPermissions.find_one()
	sharing_level = permissions['overall_sharing_level']
	permitted_roles = permissions['uidRoles'][requester_sid]
	db_RA = connection["RealityAnalysis"]
	
	for role in permitted_roles:
   	    if (db_RA.mapping.count({"ROLE":role, "LEVEL": sharing_level, "PURPOSE": "realit_analysis_share_results_read"}) > 0):
	        #Get Activity
                ha_query_result = db.funf_data.find({'PROBE':'edu.mit.media.funf.probe.builtin.ActivityProbe'})
                for row in ha_query_result:
                    total += str(row)
          
                #Get Screen 
                sc_query_result = db.funf_data.find({'PROBE':'edu.mit.media.funf.probe.builtin.ScreenProbe'})
                for row in sc_query_result:
                    total += str(row)
    except Error as e:
	logging.debug(e)
    finally:
        connection.disconnect()
    return total


def reality_analysis_share_results_readprobe(pk,pds_sid,probe):
    total = ""
    try:
	pds_id = sid_to_id(pds_sid)
	requester_sid = id_to_sid(pk)
        connection = pymongo.Connection()
        db = connection["User_" + pds_id]
	permissions = db.personalPermissions.find_one()
	sharing_level = permissions['overall_sharing_level']
	permitted_roles = permissions['uidRoles'][requester_sid]
	db_RA = connection["RealityAnalysis"]
	
	for role in permitted_roles:
   	    if (db_RA.mapping.count({"ROLE":role, "LEVEL": sharing_level, "PURPOSE": "realit_analysis_share_results_read"}) > 0):
	        #Get Activity
                ha_query_result = db.funf_data.find({'PROBE':'edu.mit.media.funf.probe.builtin.ActivityProbe'})
                for row in ha_query_result:
                    total += str(row)
          
                #Get Screen 
                sc_query_result = db.funf_data.find({'PROBE':'edu.mit.media.funf.probe.builtin.ScreenProbe'})
                for row in sc_query_result:
                    total += str(row)
    except Error as e:
	logging.debug(e)
    finally:
        connection.disconnect()
    return total


def reality_analysis_results_read(db):
    logging.debug("getting results...")
    total = ""
    try:
	#Get Activity
        ha_query_result = db.funf_data.find({'PROBE':'edu.mit.media.funf.probe.builtin.ActivityProbe'})
        for row in ha_query_result:
            total += str(row)
        
        #Get Screen 
        sc_query_result = db.funf_data.find({'PROBE':'edu.mit.media.funf.probe.builtin.ScreenProbe'})
        for row in sc_query_result:
             total += str(row)
    except Error as e:
	logging.debug(e)
    finally:
        logging.debug(total)
    return total



def reality_analysis_results_readprobe(db, probe):
    logging.debug("getting proberesults...")
    total = {}
    results = ""
    try:
	#Get Activity
	logging.debug('probe')
	logging.debug(probe)
	for result in db.funf_data.find({'PROBE':probe}):
	    #total += str(result)
	    
	    total = json.dumps(result, default=json_util.default)
    except Error as e:
	logging.debug(e)
    finally:
        logging.debug(total)
    return total

# def goetResultltin.s(request):
#     logging.debug('get results')
#     
#     #validate REST
#     scope = AccessRange.objects.get(key="reality_analysis")
#     authenticator = JSONAuthenticator(scope=scope)
# 
#     try:
#         authenticator.validate(request)
#     except AuthenticationException:
# 	logging.debug(authenticator.error_response())
#         return authenticator.error_response()
# 
#     result = ""
#     #validate permissions
#     try:
#     	pk = str(authenticator.user.pk)
# 	if request.GET.__contains__('datastore_owner'):
# 	    pds_id = request.GET['datastore_owner']
# 	    result = reality_analysis_share_results_read(pk, pds_id)
# 	else:
# 	    result = reality_analysis_results_read(pk)
# 
# 	# connecting to Mongo
# 	connection = pymongo.Connection()
# 	db = connection["User_" + pk]
#         logCollection = db.log
# 	al_entry = al_log(request.path, str(scope), False, datastore_owner, pk, purpose, tf_request)
# 	
# 	al_entry['trust_wrapper_result'] = 'allow'
# 	logCollection.insert(al_entry)
#     finally:
#         connection.disconnect()
#         return authenticator.response(result)
# 
#     # log REST success!
#     # log TF success!
#     return authenticator.response({ "success": False})

def changeRolePermissions(request):
    logging.debug('change role permissions')
    scope = AccessRange.objects.get(key="funf_write")
    authenticator = JSONAuthenticator(scope=scope)
    try:
        authenticator.validate(request)
    except AuthenticationException:
	logging.debug(authenticator.error_response())
        return authenticator.error_response()
    return authenticator.response({ "success":True})
 
def changeRolePermissions(request):
    logging.debug('change role permissions')
    scope = AccessRange.objects.get(key="funf_write")
    authenticator = JSONAuthenticator(scope=scope)
    try:
        authenticator.validate(request)
    except AuthenticationException:
	logging.debug(authenticator.error_response())
        return authenticator.error_response()
        
    try:
        (connection, db) = connectToMongoDB(str(authenticator.user.pk))
        pp = findOrCreate('personalPermissions', db, emptyPersonalPermissions)
        if request.method == 'GET':
            if request.GET.__contains__('family'):
                pp = setPermission('family', pp, request.GET['family'] == 'true')
            if request.GET.__contains__('peers'):
                pp = setPermission('peers', pp, request.GET['peers'] == 'true')
            if request.GET.__contains__('care_team'):
                pp = setPermission('care_team', pp, request.GET['care_team'] == 'true')
            db.personalPermissions.save(pp)
    finally:
        connection.disconnect()
        
        return authenticator.response({
            "success":True})
    return authenticator.response({ "success": False})
    
def changeSharingLevel(request):
    scope = AccessRange.objects.get(key="funf_write")
    authenticator = JSONAuthenticator(scope=scope)
    try:
        authenticator.validate(request)
    except AuthenticationException:
        return authenticator.error_response()
        
    try:
        (connection, db) = connectToMongoDB(str(authenticator.user.pk))
        pp = findOrCreate('personalPermissions', db, emptyPersonalPermissions)
        if request.method == 'GET' and request.GET.__contains__('level'):
            level = int(request.GET['level'])
            if level >= 0 and level <= 3:
                pp['overall_sharing_level'] = level
                db.personalPermissions.save(pp)
                return authenticator.response({"success": True})
    finally:
        connection.disconnect()
    return authenticator.response({"success": False})
    
    
    
def changeFunfConfig(request):
    scope = AccessRange.objects.get(key="funf_write")
    authenticator = JSONAuthenticator(scope=scope)
    try:
        authenticator.validate(request)
    except AuthenticationException:
        return authenticator.error_response()
    logging.debug('passed authentication')
        
    try:
        (connection, db) = connectToMongoDB(str(authenticator.user.pk))
        fconfig = findOrCreate('funf', db, emptyFunf)
        pp = findOrCreate('personalPermissions', db, emptyPersonalPermissions)
        
        if request.method == 'GET' and request.GET.__contains__('activity') and request.GET.__contains__('focus') and request.GET.__contains__('social'):
            fid = request.GET['fid']
            logging.debug('fid:'+fid)
            activity = (request.GET['activity'] == 'true')
            focus = (request.GET['focus'] == 'true')
            social = (request.GET['social'] == 'true')
            
            logging.debug('connect to user\'s personal store')
            
            fconfig['activity'] = activity
            fconfig['focus'] = focus
            fconfig['social'] = social
            if request.GET.__contains__("funf_key"):
                fconfig['funf_key'] = request.GET['funf_key']
            db.funf.save(fconfig)
            
            logging.debug('disconnect to user\'s personal store')
            logging.debug('change funf config compelte')
            
        logging.debug('about to build funf config')
        config = buildConfigFile(fconfig, pp)
    finally:
        connection.disconnect()
    logging.debug('funf config:' + str(config))
        
    return authenticator.response(config)
    
def buildConfigFile(fconfig, pp):
    config = {}
    config['name'] = 'DCAPS_Prototype'
    config['version'] = 1
    config['configUpdateUrl'] = "http://dcapsdev.media.mit.edu/api/changeFunfConfig"
    config["configUpdatePeriod"] =600 
    config["dataArchivePeriod"] = 600
    config["dataUploadUrl"] = "http://dcapsdev.media.mit.edu/api/data"
    config["dataUploadPeriod"] = 600
    dataRequests = {}
    if pp['overall_sharing_level'] > 0:
        if fconfig['activity'] == True:
            dataRequests["edu.mit.media.funf.probe.builtin.ActivityProbe"] = [{ "PERIOD": 15, "DURATION": 15 }]
        if fconfig['focus'] == True:
            dataRequests["edu.mit.media.funf.probe.builtin.ScreenProbe"] = [{}]
        if fconfig['social'] == True:
            dataRequests["edu.mit.media.funf.probe.builtin.SMSProbe"] = [{ "PERIOD": 60 }]
            dataRequests["edu.mit.media.funf.probe.builtin.CallLogProbe"] = [{ "PERIOD": 60 }]
    config['dataRequests'] = dataRequests
    return config

def getDefaults(request):
    logging.debug('GetDefaults')
    scope = AccessRange.objects.get(key="funf_write")
    authenticator = JSONAuthenticator(scope=scope)
    logging.debug(authenticator)
    logging.debug(scope)
    try:
        authenticator.validate(request)
    except AuthenticationException:
        return authenticator.error_response()
    logging.debug('try/catch') 
    
    defaults = {}
    try:
        # (connection, db) = connectToMongoDB(str(authenticator.user.pk))
        # connecting to Mongo
        connection = pymongo.Connection()
        db = connection["User_" + str(authenticator.user.pk)]
        fconfig = findOrCreate('funf', db, emptyFunf)
        pp = findOrCreate('personalPermissions', db, emptyPersonalPermissions)
        defaults = getDefaultsDict(fconfig, pp)
	pp['roles']['family'] = defaults['family']
	pp['roles']['peers'] = defaults['peers']
	pp['roles']['care_team'] = defaults['care_team']
	fconfig['activity'] = defaults['activity']
	fconfig['social'] = defaults['social']
	fconfig['focus'] = defaults['focus']
	db.personalPermissions.save(pp)
	db.funf.save(fconfig)	
    except Exception, e:
        logging.debug( "Error: %s" % str(e) )
    finally:
        connection.disconnect()
    return authenticator.response(defaults)

def getDefaultsDict(fconfig, pp):
    defaults = {}
    defaults['level'] = 0 
    defaults['focus'] = fconfig['focus']
    defaults['activity'] = fconfig['activity']
    defaults['social'] = fconfig['social']
    roles = pp['roles']
    defaults['family'] = roles.get('family', True)
    defaults['peers'] = roles.get('peers', True)
    defaults['care_team'] = roles.get('care_team', True)
    return defaults

def isTokenValid(request):
    logging.debug('validating access token')
    scope = AccessRange.objects.get(key="funf_write")
    authenticator = JSONAuthenticator(scope=scope)
    try:
        authenticator.validate(request)
    except AuthenticationException:
        return authenticator.error_response()
    return authenticator.response({})
    

def data(request):
    scope = AccessRange.objects.get(key="reality_analysis")
    authenticator = JSONAuthenticator(scope=scope)
    try:
        authenticator.validate(request)
    except AuthenticationException:
        return authenticator.error_response()
    logging.debug('receiving data')
    for filename, file in request.FILES.items():
        logging.debug('in')

        pk = str(authenticator.user.pk)
	#pk = "12"
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
            

    return authenticator.response({})
    
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
    collection = db.personalPermissions
    out = collection.find_one()
    return out['overall_sharing_level']

def get_personal_sharing_levels(pk):
    connection = pymongo.Connection()
    db = connection["User_" + pk]
    collection = db.funf
    out = collection.find_one()
    return out

def get_sharing_groups(pk):
    connection = pymongo.Connection()
    db = connection["User_" + pk]
    collection = db.personalPermissions
    out = collection.find_one()
    return out

    
@csrf_exempt
def viz(request):
    key = "funf_write"
    scope = AccessRange.objects.get(key="funf_write")
    logging.debug('post-access')
    authenticator = JSONAuthenticator(scope=scope)
    logging.debug('post-authentication')
    try:
        authenticator.validate(request)
    except AuthenticationException:
        return authenticator.error_response()
    logging.debug('visualizing data')
    pk = str(authenticator.user.pk)
    logging.debug('post-auth')
    if pk:#uuid and appToken and appTime:
        #ACCESS THE API!!!
        #values = {'uuid' : uuid,
        #          'appToken' : appToken,
        #          'appTime' : appTime}
        #data = urllib.urlencode(values)

        try:
	    
       	    levels = get_personal_sharing_levels(pk)
	    groups = get_sharing_groups(pk)
    	    connection = pymongo.Connection()
	    db = connection["User_" + pk]
	    
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
	    if sl == 0:
		activity_string = ""
		focus_string = ""
		social_ave = 0
		activity_ave = 0
		focus_ave = 0
	    elif sl == 1:
		social_score = 1	
		focus_ave = 0
		social_ave = 0
		activity_ave = 0
	    elif sl == 2:
		averages = get_averages(connection,pk)
		social_ave = 1 
		activity_ave = averages['HA']
		focus_ave = averages['SC']
		social_score = 1	
	    elif sl == 3:
		averages = get_averages(connection,pk)
		activity_ave = averages['HA']
		focus_ave = averages['SC']
		social_ave = 1
		social_score = 1	


            #Calculate scores for Activity and Focus
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
	if groups['roles']['peers'] is False:
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
    while i < num_datastores:
	try:
          i += 1
          db = connection["User_" + str(i)]
          hours_ago = time.time() -  (60*60*3*24)
          #Get Activity
          ha_query_result = db.funf_data.find({'PROBE':'edu.mit.media.funf.probe.builtin.ActivityProbe'}, {'TIMESTAMP': {'$gt': hours_ago}, 'HIGH_ACTIVITY_INTERVALS':1})
          for row in ha_query_result:
	    HA_num += row['HIGH_ACTIVITY_INTERVALS']
	    HA_den += 1
          
          #Get Screen 
	  sc_query_result = db.funf_data.find({'PROBE':'edu.mit.media.funf.probe.builtin.ScreenProbe', 'TIMESTAMP': {'$gt': hours_ago}, 'SCREEN_ON': True}, {'SCREEN_ON':1})
	  for row in sc_query_result:
	    SC_num += row['SCREEN_ON']
	    SC_den += 1
	  if SC_den == 0:
	    SC_den = 1
        except Exception as ex:
	   logging.debug(ex.args)


    sc_ave = (SC_num+ 0.0)/SC_den
    ha_ave = (HA_num+ 0.0)/HA_den
  #  sc_ave = sc_ave*5
   # ha_ave = ha_ave*5
    average = {"HA": ha_ave, "SC": sc_ave, "SO": 1} 

    levels = get_personal_sharing_levels(pk)
    return average
   
def focus_binning():
    i = 0
    return 0 
