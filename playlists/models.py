from django.db import models
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError

from music.models import Song

class Playlist(models.Model):
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="playlists"
    )
    title = models.CharField(max_length=100, null=False)
    songs = models.ManyToManyField(Song, related_name="playlists", blank=True)
    shared_with = models.ManyToManyField(
        User,
        related_name="shared_playlists",
        blank=True
    )

    def clean(self):
        """
        Проверяем ограничение: не более 3 плейлистов на одного пользователя.
        """
        if not self.pk and self.owner.playlists.count() >= 3:  # Проверяем только при создании
            raise ValidationError('Вы не можете создать более 3 плейлистов.')

    def __str__(self):
        return f"{self.title} (Owner: {self.owner.username})"
