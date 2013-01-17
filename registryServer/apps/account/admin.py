from oauth2app.models import *
from apps.account.models import *
from django.contrib import admin

admin.site.register(Profile)
class AccessTokenAdmin(admin.ModelAdmin):
	list_display = ('token', 'client', 'user')

admin.site.register(AccessToken, AccessTokenAdmin)
class AccessRangeAdmin(admin.ModelAdmin):
	list_display = ('key', 'description')
	class Meta:
		verbose_name = 'scope'

admin.site.register(AccessRange, AccessRangeAdmin)
class ClientAdmin(admin.ModelAdmin):
	list_display = ('name', 'description')

admin.site.register(Client, ClientAdmin)
admin.site.register(Code)
admin.site.register(UserToUser)
admin.site.register(Group)
