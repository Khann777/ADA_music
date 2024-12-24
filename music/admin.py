from django.contrib import admin
from .models import Song

class SongAdmin(admin.ModelAdmin):
    list_display = ['id','title','author']
    list_filter = ['title']
    search_fields = ['title']

admin.site.register(Song, SongAdmin)