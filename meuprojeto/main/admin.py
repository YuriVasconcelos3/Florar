from django.contrib import admin

from .models import *


class PostAdmin(admin.ModelAdmin):
    list_display = ('display_id','title', 'image', 'slug', 'status', 'created_on')
    list_filter = ('status',)
    search_field = ('title','content')


admin.site.register(Post, PostAdmin)