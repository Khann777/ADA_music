from rest_framework import serializers

from reviews.models import Review
from reviews.serializers import ReviewSerializer
from .models import Song

class SongSerializer(serializers.ModelSerializer):
    review_count = serializers.SerializerMethodField()

    class Meta:
        model = Song
        fields = '__all__'

    def validate_duration(self, value):
        if value < 0: 
            raise serializers.ValidationError('Длительность не может быть отрицательной')
        return value

    def get_review_count(self, instance):
        return instance.reviews.count()