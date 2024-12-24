from django.shortcuts import render
from .models import Song
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse

from .serializers import SongSerializer

def get_song(request):
    if request.method == 'GET':
        songs = Song.objects.all()
        data = []
        for song in songs:
            data.append({
                'id': song.id,
                'title': song.title,
                'author': song.author,
                'duration': song.duration,
                'genre': song.genre
            })
        return JsonResponse(data, safe=False)
    
class CreateSong(APIView):
    def create(self, request):
        serializer = SongSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class DeleteSong(APIView):
    def delete(self, request, pk):
        song = Song.objects.filter(pk=pk).first()
        if not song:
            return Response({'msg': 'Песня не найдена'}, status=status.HTTP_404_NOT_FOUND)
        song.delete()
        return Response({'msg': 'Песня удалена'}, status=status.HTTP_204_NO_CONTENT)
    
class UpdateSong(APIView):
    def patch(self, request, pk):
        try:
            song = Song.objects.get(pk=pk)
        except Song.DoesNotExist:
            return Response({'msg': 'Песня не найдена'}, status=status.HTTP_404_NOT_FOUND)

        serializer = SongSerializer(song, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
    