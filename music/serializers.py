from rest_framework import serializers
from django.db.models import Avg

from .models import Song

class SongSerializer(serializers.ModelSerializer):
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Song
        fields = '__all__'

    def validate_duration(self, value):
        if value < 0: 
            raise serializers.ValidationError('Длительность не может быть отрицательной')
        return value

    def get_average_rating(self, instance):
        """
        Рассчитывает средний рейтинг песни на основе связанных отзывов.
        """
        reviews = instance.reviews.all()
        if reviews.exists():
            return reviews.aggregate(Avg('rating'))['rating__avg']
        return 0  # Если отзывов нет, средний рейтинг равен 0
