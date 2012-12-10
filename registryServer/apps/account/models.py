from django.db import models
from django.contrib.auth.models import User
import settings
from oauth2app.models import Client
import uuid

#def create_profile_for_user(user):
#   '''utility function for creating a user, client and profile necessary for instantiating a PDS with a Trust Network'''
#  pds_ip = settings.pdsDefaultIP
#  pds_port = settings.pdsDefaultPort
#  new_client = Client(name=user.username+"_pds", user=user, description="user "+user.username+"'s Personal Data Store", redirect_uri="http://"+pds_ip+":"+pds_port+"/?username="+user.username)
#  new_client.save()
#  new_profile = Profile(user=user, pds_ip=pds_ip, pds_port=pds_port, pds_client=new_client)
#  new_profile.save()
#  return new_profile

class Profile(models.Model):
  user = models.ForeignKey(User, unique=True)
  group = models.ForeignKey('Group', blank=True, null=True)
#  pds_location = models.URLField(max_length=100, default=str(settings.pdsDefault))
  pds_ip = models.GenericIPAddressField(default=str(settings.pdsDefaultIP))
  pds_port = models.PositiveIntegerField(default=str(settings.pdsDefaultPort))
#  pds_client = models.ForeignKey(Client, unique=True)
  uuid = models.CharField(max_length=36, unique=True, default=uuid.uuid4)
  def __unicode__(self):
    return self.user.username
  def set_default_client(self):
    new_client = Client(name=self.user.username+"_pds", user=self.user, description="user "+self.user.username+"'s Personal Data Store", redirect_uri="http://"+self.pds_ip+":"+self.pds_port+"/?username="+self.user.username)
    new_client.save()
#    self.pds_client = new_client
     
PERMISSION = (
  ('r','Read'),
  ('w', 'Write'),
  ('rw', 'Read Write'),
)

class Group(models.Model):
  name = models.CharField(max_length=100, unique=True)
  def __unicode__(self):
    return self.name
    
class UserToUser(models.Model):
  profileGuest = models.ForeignKey(Profile, related_name='guest')
  profileHost = models.ForeignKey(Profile, related_name='host')
  role = models.CharField(max_length=100)
  class Meta:
    unique_together = (("profileGuest", "profileHost", "role"))
