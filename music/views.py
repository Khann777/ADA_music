from django.shortcuts import render
from .models import Song
from rest_framework import generics
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from .serializers import SongSerializer

class SongCreateView(generics.CreateAPIView):
    permission_classes = (IsAdminUser)
    serializer_class = SongSerializer


class SongListView(generics.ListAPIView):
    queryset = Song.objects.all()
    serializer_class = SongSerializer

class SongUpdateView(generics.UpdateAPIView):
    permission_classes = (IsAdminUser)
    queryset = Song.objects.all()
    serializer_class = SongSerializer

class SongDeleteView(generics.DestroyAPIView):
    permission_classes = (IsAdminUser)
    queryset = Song.objects.all()