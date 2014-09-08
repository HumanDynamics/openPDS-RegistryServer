from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
import settings
from oauth2app.models import Client
import uuid

class Profile(models.Model):
  user = models.ForeignKey(User, unique=True)
  pds_location = models.URLField(max_length=100, default=str(settings.pdsDefaultLocation))
  funf_password = models.CharField(max_length=100, default="changeme")
  uuid = models.CharField(max_length=36, unique=True, default=uuid.uuid4)
  def __unicode__(self):
    return "%s - %s"%(self.user.username, self.uuid)
  def set_default_client(self):
    new_client = Client(name=self.user.username+"_pds", user=self.user, description="user "+self.user.username+"'s Personal Data Store", redirect_uri="http://"+self.pds_location + "/?username="+self.user.username)
    new_client.save()
#    self.pds_client = new_client

def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

post_save.connect(create_profile, sender=User)
     
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
