from django.contrib import admin
from .models import Posts, Comments


class PostAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'title', 'time']


admin.site.register(Posts, PostAdmin)
admin.site.register(Comments)
