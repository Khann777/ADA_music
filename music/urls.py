from django.urls import path
from .views import (
    ReviewAddView, SongListView, SongDetailView,
    SongUpdateView, SongDeleteView, SongCreateView
)

urlpatterns = [
    path('music/', SongCreateView.as_view(), name='song-create'),  # POST для создания песни
    path('music/list/', SongListView.as_view(), name='song-list'),
    path('music/<int:pk>/', SongDetailView.as_view(), name='song-detail'),
    path('music/<int:pk>/update/', SongUpdateView.as_view(), name='song-update'),
    path('music/<int:pk>/delete/', SongDeleteView.as_view(), name='song-delete'),

    # Отзывы
    path('music/<int:song_id>/review/', ReviewAddView.as_view(), name='add-review'),
]
