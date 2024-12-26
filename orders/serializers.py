from rest_framework import serializers

from .models import Order

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')

    def validate_file(self, value):
        if value is None:
            raise serializers.ValidationError('File must be provided')
        if value.size < 10*1024*1024:
            raise serializers.ValidationError('File must be smaller than 10MB')
        if not value.filename.endswith('.mp3', '.wav', '.m4a', '.m4p'):
            raise serializers.ValidationError('File must have .mp3, .wav, .m4a, .m4p extension')
        return value

    def validate_status(self, value):
        valid_statuses = [choice[0] for choice in Order.STATUS_CHOICES]
        if value not in valid_statuses:
            raise serializers.ValidationError(f'Invalid status {value}, choose from {valid_statuses}')
        return value

    def validate(self, data):
        if data.get('status') == 'completed' and not data.get('file'):
            raise serializers.ValidationError('File must be provided')
        return data
