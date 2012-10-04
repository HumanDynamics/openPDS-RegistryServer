from django.contrib.auth.models import User
from apps.account.models import Profile, Group
from tastypie import fields
from tastypie.authorization import DjangoAuthorization
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS

class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
#	excludes = ['is_staff', 'is_superuser', 'last_login', 'password', 'date_joined']

class ProfileResource(ModelResource):
    class Meta:
        queryset = Profile.objects.all()
#	excludes = ['is_staff', 'is_superuser', 'last_login', 'password', 'date_joined']

class GroupResource(ModelResource):
    class Meta:
        queryset = Group.objects.all()
#	excludes = ['is_staff', 'is_superuser', 'last_login', 'password', 'date_joined']

