from mongoengine import *

class FunfData(Document):
  data = BinaryField()
