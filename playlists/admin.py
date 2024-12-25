from django.contrib import admin
from .models import Playlist

class PlaylistAdmin(admin.ModelAdmin):
    list_display = ['name','owner']
    list_filter = ['name']
    search_fields = ['name']

admin.site.register(Playlist, PlaylistAdmin)
