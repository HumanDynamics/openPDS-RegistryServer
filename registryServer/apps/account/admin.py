from oauth2app.models import *
from apps.account.models import *
from django.contrib import admin

admin.site.register(Profile)
admin.site.register(AccessToken)
class AccessRangeAdmin(admin.ModelAdmin):
	list_display = ('key', 'description')
	class Meta:
		verbose_name = 'scope'

admin.site.register(AccessRange, AccessRangeAdmin)
admin.site.register(Client)
admin.site.register(Code)
admin.site.register(UserToUser)
admin.site.register(Group)
