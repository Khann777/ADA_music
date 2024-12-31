from django.contrib.auth.models import User
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action

from django.shortcuts import get_object_or_404
from .models import Playlist
from .serializers import PlaylistSerializer
from music.models import Song
from account.permissions import IsOwner


class PlaylistViewSet(viewsets.ModelViewSet):
    """
    Viewset for playlists
    """
    serializer_class = PlaylistSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """
        Админ видит все плейлисты, а обычные пользователи только свои.
        """
        if self.request.user.is_staff:
            return Playlist.objects.all()
        return Playlist.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        """
        Устанавливаем текущего пользователя как владельца плейлиста.
        """
        serializer.save(owner=self.request.user)

    def get_permissions(self):
        """
        Определяем права доступа для действий.
        """
        if self.action in ['update', 'partial_update', 'destroy', 'add_song', 'remove_song', 'share', 'revoke_access']:
            return [IsOwner()]
        return super().get_permissions()

    @action(detail=True, methods=['post'])
    def add_song(self, request, pk=None):
        playlist = self.get_object()
        song_id = request.data.get('song_id')
        song = get_object_or_404(Song, pk=song_id)
        if song in playlist.songs.all():
            return Response({"detail": f"Song - {song.title} already in playlist {playlist.title}."}, status=status.HTTP_400_BAD_REQUEST)
        playlist.songs.add(song)
        return Response({"detail": f"Song - {song.title} added to playlist - {playlist.title}"}, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def remove_song(self, request, pk=None):
        playlist = self.get_object()
        song_id = request.data.get('song_id')
        song = get_object_or_404(Song, pk=song_id)
        if song not in playlist.songs.all():
            return Response({"detail": f"Song - {song.title} not in playlist - {playlist.title}."}, status=status.HTTP_400_BAD_REQUEST)
        playlist.songs.remove(song)
        return Response({"detail": f"Song - {song.title} removed from playlist - {playlist.title}"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def share(self, request, pk=None):
        playlist = self.get_object()
        username = request.data.get('username')
        user = get_object_or_404(User, username=username)
        if user in playlist.shared_with.all():
            return Response({"detail": f"User {username} already has access to playlist - {playlist.title}."}, status=status.HTTP_400_BAD_REQUEST)
        playlist.shared_with.add(user)
        return Response({"detail": f"Playlist shared with {username} for playlist - {playlist.title}."}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def revoke_access(self, request, pk=None):
        playlist = self.get_object()
        username = request.data.get('username')
        user = get_object_or_404(User, username=username)
        if user not in playlist.shared_with.all():
            return Response({"detail": f"User {username} does not have access to playlist - {playlist.title}."}, status=status.HTTP_400_BAD_REQUEST)
        playlist.shared_with.remove(user)
        return Response({"detail": f"Access revoked for {username} from playlist - {playlist.title}."}, status=status.HTTP_200_OK)
