from django.db import models
from django.contrib.auth.models import User  
from rest_framework.permissions import IsAdminUser, IsAuthenticated
class Playlist(models.Model):
    
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='playlists')
    songs = models.ManyToManyField('music.Song', related_name='playlists', blank=True)


    def __str__(self):
        return f'{self.name} (Владелец: {self.owner.username})'

