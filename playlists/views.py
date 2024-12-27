from django.shortcuts import render
from .models import Playlist
from rest_framework.response import Response
from rest_framework import viewsets, permissions, status
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.decorators import action
from .serializers import PlaylistSerializer
from music.views import Song

class PlaylistViewSet(viewsets.ModelViewSet):
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer
    ADMIN_ACTIONS = ['create', 'update', 'destroy', 'approve', 'reject']


    def get_permissions(self):
        if self.action in self.ADMIN_ACTIONS:
            return [IsAdminUser()]
        return [permissions.IsAuthenticated()]
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)   


    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Playlist.objects.all()
        return Playlist.objects.filter(owner=user)
    

    @action(detail=True, methods=['POST'])
    def add_song(self, request, pk=None):
        playlist = self.get_object()
        song_ids = request.data.get('songs', [])

        if not song_ids:
            return Response({'msg': 'Не переданы песни'}, status=status.HTTP_400_BAD_REQUEST)
        
        songs = Song.objects.filter(id__in=song_ids)
        if songs.count() != len(set(song_ids)):
            return Response({'msg': 'Некоторые песни не найдены'}, status=status.HTTP_404_NOT_FOUND)

        for song in songs:
            if song not in playlist.songs.all():
                playlist.songs.add(song)

        serializer = PlaylistSerializer(playlist)
        return Response(serializer.data, status=status.HTTP_200_OK)


    @action(detail=True, methods=['DELETE'])
    def delete_from_playlist(self, request, pk=None):
        playlist = self.get_object()
        song_ids = request.data.get('songs', [])

        if not song_ids:
            return Response({'msg': 'Не переданы песни'}, status=status.HTTP_400_BAD_REQUEST)

        songs_ = playlist.songs.filter(id__in=song_ids)
        if songs_.count() != len(set(song_ids)):
            return Response({'msg': 'Некоторые песни не найдены'}, status=status.HTTP_404_NOT_FOUND)

        playlist.songs.remove(*songs_)
        return Response({'msg': 'Песни успешно удалены из плейлиста'}, status=status.HTTP_200_OK)
