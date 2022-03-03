from django.contrib import admin
from .models import MessageOrder, Messages, NotificationFollower, NotificationComment, Activity, Settings


# Register your models here.
admin.site.register(MessageOrder)
admin.site.register(Messages)
admin.site.register(Settings)

class NotificationFollowerAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'is_read']
    list_editable = ['is_read']


admin.site.register(NotificationFollower, NotificationFollowerAdmin)


class NotificationCommentrAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'is_read']
    list_editable = ['is_read']


admin.site.register(NotificationComment, NotificationCommentrAdmin)

admin.site.register(Activity)
