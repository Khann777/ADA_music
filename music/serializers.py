from rest_framework import serializers
from .models import Song

class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = '__all__'

    def validate_duration(self, value):
        if value < 0: 
            raise serializers.ValidationError('Длительность не может быть отрицательной')
        return value
