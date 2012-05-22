from oauth2app.models import *
from apps.account.models import *
from django.contrib import admin

admin.site.register(Profile)
admin.site.register(AccessRange)
admin.site.register(AccessToken)
admin.site.register(Client)
admin.site.register(Code)
admin.site.register(UserToUser)
admin.site.register(Group)
