from django.contrib import admin
from django.contrib.messages import api
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('account.urls')),
    path('music/', include('music.urls')),
    path('playlists/', include('playlists.urls')),
]
