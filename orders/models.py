from django.db import models

class Order(models.Model):
    song = models.CharField(max_length=100, null=False, blank=False)
    author = models.CharField(max_length=100, null=False, blank=False)
    file = models.FileField(upload_to='uploads/', null=False, blank=False)
    customer = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name='orders')
    STATUS_CHOICES = [
        ('pending', 'В обработке'),
        ('approved', 'Одобрено'),
        ('rejected', 'Отклонено'),
    ]
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



    def __str__(self):
        return f'{self.author} - {self.song}'
