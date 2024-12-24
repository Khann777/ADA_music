from django.db import models

class Song(models.Model):
    title = models.CharField(max_length=50)
    author = models.CharField(max_length=50)
    duration = models.IntegerField()
    genre = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.author} - {self.author}'
    

        