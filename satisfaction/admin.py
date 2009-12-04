from satisfaction_site.satisfaction.models import *
from django.contrib import admin

class VideoAdmin(admin.ModelAdmin):
	
	fieldsets = [
		( None, 	{'fields': ['name','description','url','category','user']}),
	]

	list_filter = ['name']
	search_fields = ['name']
	

admin.site.register(Video,VideoAdmin)
admin.site.register(Category)
admin.site.register(Tag)
