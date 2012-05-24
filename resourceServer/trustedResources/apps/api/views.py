#-*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
import urllib
import urllib2
import hashlib
import datetime
import numpy as np

from oauth2app.authenticate import JSONAuthenticator, AuthenticationException
from django.http import HttpResponse
from oauth2app.models import AccessRange
#from account.models import *
from mongoengine import *
from datastoreModels import *
from django.utils import simplejson as json
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

upload_dir = '/data/temp'

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
#	logging.debug(authenticator.error_response())
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



def getResults(request):
    logging.debug('get results')
    import pydevd;pydevd.settrace('18.189.24.242',stdoutToServer=True, stderrToServer=True,port=5679)
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
            db = connection["User_5"]
            if tw_result:
                if request.GET.__contains__('probe'):
                    logging.debug('calling readprobe')
                    result = reality_analysis_results_readprobe(db,request.GET['probe'])
                else:
		    logging.debug('calling read')
                    result = reality_analysis_results_read(db)


        # connecting to Mongo
        #logCollection = db.log
        #al_entry = al_log(request.path, str(scope), False, datastore_owner, pk, purpose, tf_request)

        #al_entry['trust_wrapper_result'] = 'allow'
        #logCollection.insert(al_entry)
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


def reality_analysis_results_read(db):
    logging.debug("getting results...")
    response = ""
    try:
        #Get Activity
        query_results = db.funf_data.find()
        for result in query_results:
	    logging.debug(result)
            response += json.dumps(result, default=json_util.default)

    except Error as e:
        logging.debug(e)
    finally:
        logging.debug(response)
    return response



def reality_analysis_results_readprobe(db, probe):
    response = ""
    try:
        #Get Activity
	query_results = db.funf_data.find({'PROBE':probe})
        for result in query_results:
            response += json.dumps(result, default=json_util.default)
    except Error as e:
        logging.debug(e)
    finally:
        logging.debug(response)
    return response


def setPermission(name, pp, permission):
    roles = pp['roles']
    roles[name] = permission
    return pp

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
    scope = AccessRange.objects.get(key="funf_write")
    authenticator = JSONAuthenticator(scope=scope)
    try:
        authenticator.validate(request)
    except AuthenticationException:
        return authenticator.error_response()
    return authenticator.response({})
    

def data(request):
    scope = AccessRange.objects.get(key="funf_write")
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
    key = "reality_analysis"
    scope = AccessRange.objects.get(key="reality_analysis")
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

	    #log entry 	    
      	    db_log = findOrCreate('log', db, emptyLog)
	    db_log_entry

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
