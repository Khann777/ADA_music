from django.urls import path
from .views import PlaylistCreate, PlaylistDeleteView, PlaylistDetailView, PlaylistListView, PlaylistUpdateView, AddToPlaylist, DeleteFromPlaylist

urlpatterns = [
    path('playlist-list/', PlaylistListView),
    path('playlist-delete/<int:pk>/', PlaylistDeleteView.as_view()),
    path('playlist-create/',PlaylistCreate.as_view()),
    path('playlist-update/<int:pk>/', PlaylistUpdateView.as_view()),
    path('playlist-detail/<int:pk>/', PlaylistDetailView.as_view()),
    path('playlist-add-song/<int:pk>/', AddToPlaylist.as_view()),
    path('playlist-delete-song/<int:pk>/', DeleteFromPlaylist.as_view())
    ]