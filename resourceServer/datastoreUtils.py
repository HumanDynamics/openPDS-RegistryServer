import pymongo

def connectToMongoDB(pk):
    connection = pymongo.Connection()
    db = connection["User_" +pk]
    return (connection, db)


def emptyPersonalPermissions():
    pp = {}
    pp['overall_sharing_level'] = 3
    pp['roles'] = {}
    pp['uidRoles'] = {}
    return pp
  
def emptyFunf():
  f = {}
  f['fid'] = 1
  f['funf_key'] = "12345678"
  f['activity'] = True
  f['social'] = True
  f['focus'] = True
  return f

def findOrCreate(collection, db, emptyCollectionFunction):
  if db[collection].count() > 0:
      entity = db[collection].find_one()
  else:
      entity = emptyCollectionFunction()
      db[collection].insert(entity)
  return entity