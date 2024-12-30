from django.contrib import admin
from .models import Playlist

class PlaylistAdmin(admin.ModelAdmin):
    list_display = ['title','owner']
    list_filter = ['title', 'owner']
    search_fields = ['title', 'owner__username']

admin.site.register(Playlist, PlaylistAdmin)
