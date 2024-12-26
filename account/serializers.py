from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('password',)
        read_only_fields = ['id']

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True, min_length=8, required=True)
    password_confirm = serializers.CharField(style={'input_type': 'password'}, write_only=True, min_length=8, required=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'password_confirm', 'first_name', 'last_name']

    def validate(self, attrs):
        password = attrs['password']
        password_confirm = attrs.pop('password_confirm')
        if password_confirm != password:
            raise serializers.ValidationError('Passwords must match')
        validate_password(password)
        return attrs

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True, min_length=8, required=True)

    def validate(self, attrs):
        username = attrs['username']
        password = attrs['password']
        request = self.context.get('request')

        if username and password:
            user = authenticate(username=username,
                                password=password,
                                request=request)
            if not user or not user.is_active:
                raise serializers.ValidationError({
                    "error": "Invalid credentials",
                    "detail": "Username or password is incorrect, or account is inactive."
                })

        else:
            raise serializers.ValidationError('Username or password is required')

        attrs['user'] = user
        return attrs


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_active', 'date_joined', 'last_login', 'is_staff', 'is_superuser']

class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_active', 'date_joined', 'last_login', 'is_staff', 'is_superuser']


