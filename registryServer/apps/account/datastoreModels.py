from mongoengine import *

class PersonalPermissions(Document):
  overall_sharing_level = IntField(default=3)
  roles = DictionaryField(default={})
  uidRoles = ListField(default=[])
  