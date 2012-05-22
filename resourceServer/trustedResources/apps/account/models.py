from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
  user = models.ForeignKey(User, unique=True)
  group = models.ForeignKey('Group', blank=True, null=True)
  def __unicode__(self):
    return self.user.username
  
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
  class Meta:
    unique_together = (("profileGuest", "profileHost"))
