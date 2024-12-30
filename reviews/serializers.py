from rest_framework import serializers
from .models import Review
from music.models import Song

class ReviewSerializer(serializers.ModelSerializer):
    reviewer = serializers.ReadOnlyField(source='reviewer.username')  # Только для чтения
    music = serializers.ReadOnlyField(source='music.title')  # Только для чтения

    class Meta:
        model = Review
        fields = ['id', 'reviewer', 'music', 'rating']
        read_only_fields = ['id', 'reviewer', 'music']  # Эти поля не записываются

    def create(self, validated_data):
        """
        Создаем объект, исключая read-only поля.
        """
        return super().create(validated_data)


