from django.db import models
from music.models import Song
from django.contrib.auth.models import User

class Review(models.Model):
    music = models.ForeignKey(Song, on_delete=models.CASCADE, related_name='reviews')
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveSmallIntegerField()

    class Meta:
        unique_together = ('music', 'reviewer')  # Гарантируем уникальность отзыва для пользователя и песни

    def __str__(self):
        return f'Review for {self.music.title} by {self.reviewer.username} - {self.rating}'

    def save(self, *args, **kwargs):
        # Пересчет среднего рейтинга песни при сохранении отзыва
        super().save(*args, **kwargs)
        self.music.reviews.aggregate_rating()