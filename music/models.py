from django.db import models
from django.db.models import Avg

class Song(models.Model):
    title = models.CharField(max_length=50)
    author = models.CharField(max_length=50)
    duration = models.IntegerField()
    genre = models.CharField(max_length=50)
    file = models.FileField(upload_to='uploads/', null=True, blank=True)
    average_rating = models.FloatField(default=0.0)
    rating_count = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.author} - {self.title}'

    def aggregate_rating(self):
        # Пересчитываем средний рейтинг и количество отзывов
        reviews = self.reviews.all()
        if reviews.exists():
            self.average_rating = reviews.aggregate(Avg('rating'))['rating__avg']
            self.rating_count = reviews.count()
        else:
            self.average_rating = 0.0
            self.rating_count = 0
        self.save()
