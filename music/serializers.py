from rest_framework import serializers
from .models import Song

class SongSerializer(serializers.ModelSerializer):
    MAX_SIZE = 10*1024*1024
    ALLOWED_EXTENSIONS = ['.mp3', '.wav', '.m4a', '.m4p']
    class Meta:
        model = Song
        fields = '__all__'

    def validate_duration(self, value):
        if value < 0: 
            raise serializers.ValidationError('Длительность не может быть отрицательной')
        return value
    
    def validate_file(self, value):
        if value is None:
            raise serializers.ValidationError('File must be provided')
        if value.size > self.MAX_SIZE:
            raise serializers.ValidationError('File must be smaller than 10MB')
        if not any(value.name.lower().endswith(ext) for ext in self.ALLOWED_EXTENSIONS):
            allowed_ext_str = ', '.join(self.ALLOWED_EXTENSIONS)
            raise serializers.ValidationError(f'File must have one of the following extensions: {allowed_ext_str}.')
        return value
