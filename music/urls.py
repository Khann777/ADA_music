from django.urls import path
from .views import SongCreateView, SongDeleteView, SongListView, SongUpdateView

urlpatterns = [
    path('song-list/', SongListView.as_view()),
    path('song-delete/<int:pk>/', SongDeleteView.as_view()),
    path('song-create/', SongCreateView.as_view()),
    path('song-update/<int:pk>/', SongUpdateView.as_view())
    ]
