from django.contrib import admin
from . import models

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'last_name', 'email', 'is_active']
    list_editable = ['is_active']


admin.site.register(models.Profile, UserAdmin)
admin.site.register(models.Order)
admin.site.register(models.OrderDetail)
admin.site.register(models.OrderFollowing)
admin.site.register(models.OrderDetailFollowing)
admin.site.register(models.Latest_Search)
