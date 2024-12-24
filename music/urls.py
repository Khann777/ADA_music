from django.urls import path
from .views import CreateSong, DeleteSong, get_song, UpdateSong

urlpatterns = [
    path('song-list/', get_song),
    path('song-delete/<int:pk>/', DeleteSong.as_view()),
    path('song-create/', CreateSong.as_view()),
    path('song-update/<int:pk>/', UpdateSong.as_view())
    ]
