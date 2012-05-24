import pymongo
import logging
from pymongo import Connection

#TODO This trust wrapper implements sharing as defined in DARPA DCAPS project.  Eventually we will need to implement sharing fully defined at the PDS level, and not a shared database.
def trustWrapper(pk, purpose, r_sid):
    logging.debug('checking against Trust Wrapper')
    try:
        #pds_id = sid_to_id(pds_sid)
        #host = id_to_sid(pk, pds_sid)
        connection = pymongo.Connection()
	#TODO When PDS' are distributed, the database will be known implicitly
        db = connection["User_" + str(pk)]
        sharing_permissions = db.personalPermissions.find_one({'permission_type':'sharing'})
        role_permissions = db.personalPermissions.find_one({'permission_type':'roles'})
	sharing_level = 0
	permitted_roles = []

	if('sharing' in sharing_permissions):
	    sharing_settings = sharing_permissions['sharing']
	    if('overall_sharing_level' in sharing_settings):
		sharing_level = sharing_settings['overall_sharing_level']
	if('uidRoles' in sharing_permissions):
	    role_relationships = sharing_permissions['uidRoles']
	    if(str(r_sid) in role_relationships):
		permitted_roles = role_relationships[str(r_sid)]
		
		
        #sharing_level = sharing_permissions['sharing']['overall_sharing_level']
        #permitted_roles = sharing_permissions['uidRoles']#[r_sid]
	#TODO We will need to define application parameters where we can hold a list of installled applications, and create application specific stores on the fly
        db_RA = connection["RealityAnalysis"]

        for role in permitted_roles:
            if (db_RA.mapping.count({"ROLE":role, "LEVEL": sharing_level, "PURPOSE": purpose}) > 0):
                return True
    except TypeError as e:
        logging.debug('ERROR: personalPermissions store is not configured correclty.  Check that the collection "personalPermissions" exists, as well as entries for key-value "permission_type"-"sharing" as well as sub element object keys for "sharing" and "uidRoles"')
        logging.debug(e)
    finally:
        connection.disconnect()
    return False

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
        connection.disconnect()
    return False

def initializePersonalPermissions(db):
    is_upsert = True
    db.personalPermissions.update({"permission_type":"sharing"},{"sharing" : { "overall_sharing_level" : "2" }, "permission_type" : "sharing", "uidRoles": {}}, is_upsert)
    db.personalPermissions.update({"permission_type":"roles"},{"roles" : { "Care_Team" : False, "Peers" : False, "Family" : False }, "permission_type" : "roles"}, is_upsert)
    return True


#def id_to_sid(guest, host_symbolic):
#    #implement retrieval of id from symbolic id
#    prof = Profile.objects.filter(user=guest)
#    mapping = UserToUser.objects.filter(profileGuest=prof[0], id=host_symbolic)
#    if(mapping.count() == 0):
#        return {"error": "counldn't find specified symbolic mapping"}
#    elif(mapping.count() > 1):
#	return {"error": "unexpected return value"}
#    return mapping[0].profileHost


#TODO Full implementaion of PDS level sharing.
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

