from django.shortcuts import render
from .models import Playlist
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from django.http import JsonResponse
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.decorators import action
from .serializers import PlaylistSerializer

class PlaylistCreate(APIView):
    permission_classes = (IsAuthenticated)

    def post(self, request):
        serializer = PlaylistSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['owner'] = request.user
            serializer.save()
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class PlaylistListView(APIView):
    permission_classes = (IsAuthenticated)

    def get(self, request):
        playlists = Playlist.objects.filter(owner=request.user)
        serializer = PlaylistSerializer(playlists, many=True)
        return Response(serializer.data)
    

class PlaylistDetailView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated)
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer
    

class PlaylistDeleteView(generics.DestroyAPIView):
    permission_classes = (IsAuthenticated)
    queryset = Playlist.objects.all()

class PlaylistUpdateView(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated)
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer


class AddToPlaylist(ModelViewSet):
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer

    @action(detail=False, methods=['POST'])
    def add_song(self, request, pk):
        playlist = self.get_object()
        song_ids = request.data.get('songs', [])

        if not song_ids:
            return Response({'msg': 'Не переданы песни'}, status=status.HTTP_400_BAD_REQUEST)
        
        songs = Song.objects.filter(id__in=song_ids)
        if len(songs) != len(song_ids):
            return Response({'msg': 'Некоторые песни не найдены'}, status=status.HTTP_404_NOT_FOUND)

        for song in songs:
            if song not in playlist.songs.all():
                playlist.songs.add(song)

        serializer = PlaylistSerializer(playlist)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class DeleteFromPlaylist(ModelViewSet):
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer

    @action(detail=False, methods=['DELETE'])
    def delete_from_playlist(self, request, pk=None):
        playlist = self.get_object()
        song_ids = request.data.get('songs', [])

        if not song_ids:
            return Response({'msg': 'Не переданы песни'}, status=status.HTTP_400_BAD_REQUEST)

        songs = playlist.objects.filter(id__in=song_ids)
        if len(songs) != len(song_ids):
            return Response({'msg': 'Некоторые песни не найдены'}, status=status.HTTP_404_NOT_FOUND)

        playlist.songs.remove()
        

