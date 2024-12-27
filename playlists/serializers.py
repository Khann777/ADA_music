from rest_framework import serializers
from .models import Playlist
from music.views import Song

class PlaylistSerializer(serializers.ModelSerializer):
    songs = serializers.PrimaryKeyRelatedField(queryset=Song.objects.all(), many=True)  # Поле для добавления песен

    class Meta:
        model = Playlist
        fields = ['id', 'name', 'owner', 'songs']


