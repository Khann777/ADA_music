from django.db import models
from music.models import Song
from django.contrib.auth.models import User

class Review(models.Model):
    music = models.ForeignKey(Song, on_delete=models.CASCADE, related_name='reviews')
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(default=0)
    text = models.TextField(default='')

    def __str__(self):
        return f'Review for {self.music.title} by {self.reviewer.username}'
