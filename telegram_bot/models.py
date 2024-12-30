from django.db import models

class TelegramUser(models.Model):
    chat_id = models.CharField(max_length=50, unique=True)
    username = models.CharField(max_length=100, null=True, blank=True)
    is_registered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
