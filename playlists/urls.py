from django.urls import path, include

from rest_framework import routers

from playlists.views import PlaylistViewSet

router = routers.DefaultRouter()

router.register('playlists', PlaylistViewSet)

urlpatterns = [
    path('', include(router.urls)),
]