from django.db import models
from django.contrib.auth.models import User

class Script(models.Model):
  name = models.CharField(max_length=100, unique=True)
  code = models.TextField()
  def __unicode__(self):
    return self.name
  
