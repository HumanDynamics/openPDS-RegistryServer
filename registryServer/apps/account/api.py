from tastypie.resources import ModelResource
from apps.account.models import Profile
from django.contrib.auth.models import User

#TODO Decide if we should expose the profile or user model
#class ProfileResource(ModelResource):
#    class Meta:
#        queryset = Profile.objects.all()
#        resource_name = 'profile'

class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
