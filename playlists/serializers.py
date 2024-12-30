from django.contrib.auth.models import User
from rest_framework import serializers

from music.serializers import SongSerializer
from .models import Playlist


class PlaylistSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")
    songs = SongSerializer(many=True, read_only=True)
    shared_with = serializers.SlugRelatedField(
        many=True,
        slug_field="username",
        queryset=User.objects.all(),
        required=False  # Позволяем владельцам изменять список
    )

    class Meta:
        model = Playlist
        fields = ['id', 'owner', 'title', 'songs', 'shared_with']
