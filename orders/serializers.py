from rest_framework import serializers

from .models import Order

class OrderSerializer(serializers.ModelSerializer):
    MAX_SIZE = 10*1024*1024 #? Максимальный размер файла — 10MB
    ALLOWED_EXTENSIONS = ['.mp3', '.wav', '.m4a', '.m4p'] #? Разрешенные расширения файлов


    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')

    #? Проверка на правильное расширение файла
    def validate_file(self, value):
        if value is None:
            raise serializers.ValidationError('File must be provided')
        if value.size > self.MAX_SIZE:
            raise serializers.ValidationError('File must be smaller than 10MB')
        if not any(value.name.lower().endswith(ext) for ext in self.ALLOWED_EXTENSIONS):
            allowed_ext_str = ', '.join(self.ALLOWED_EXTENSIONS)
            raise serializers.ValidationError(f'File must have one of the following extensions: {allowed_ext_str}.')
        return value

    #? Проверка выбора статуса к заказу
    def validate_status(self, value):
        request = self.context.get('request')
        VALID_STATUSES = [choice[0] for choice in Order.STATUS_CHOICES]

        if value not in VALID_STATUSES:
            raise serializers.ValidationError(f'Invalid status {value}, choose from {VALID_STATUSES}')
        if value in ['approved', 'rejected'] and (not request or not request.user.is_staff):
            raise serializers.ValidationError('Only admins can change the status.')
        return value

    #? Проверка на выдачу статуса "Одобрено" только при наличии файла
    def validate(self, data):
        if data.get('status') == 'approved' and not data.get('file'):
            raise serializers.ValidationError('File must be provided')
        return data
