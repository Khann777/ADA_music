from django.db import models

class Order(models.Model):
    song = models.CharField(max_length=100, null=False, blank=False) #* Название песни
    author = models.CharField(max_length=100, null=False, blank=False) #* Имя/псевдоним автора
    file = models.FileField(upload_to='uploads/', null=False, blank=False)  #* Файл с песней
    customer = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name='orders') #* Связь с пользователем
    STATUS_CHOICES = [
        ('pending', 'В обработке'),
        ('approved', 'Одобрено'),
        ('rejected', 'Отклонено'),
    ] #* Возможные статусы
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    ) #* Статус заказа
    created_at = models.DateTimeField(auto_now_add=True) #* Дата создания
    updated_at = models.DateTimeField(auto_now=True) #* Дата обновления

    def __str__(self):
        return f'Заказ песни: {self.author} - {self.song} от {self.customer} - {self.status}'
