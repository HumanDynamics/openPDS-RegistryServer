from tastypie.resources import ModelResource
from tastypie import fields, utils
from apps.account.models import Profile
from django.contrib.auth.models import User

#TODO Decide if we should expose the profile or user model
#class ProfileResource(ModelResource):
#    class Meta:
#        queryset = Profile.objects.all()
#        resource_name = 'profile'

class UserResource(ModelResource):
    IDC_ADMIN = fields.BooleanField(default=False)    
    class Meta:
        queryset = User.objects.all()
	excludes = ['id', 'password', 'date_joined', 'is_superuser', 'is_active', 'is_staff']
        resource_name = 'user'
