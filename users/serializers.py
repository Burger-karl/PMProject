from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.core.validators import EmailValidator
from django.contrib.auth.password_validation import validate_password

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'confirm_password', 'email', 'user_type')
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'validators': [EmailValidator()]}
        }

    def validate(self, data):
        # Passwords must match
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")
        
        validate_password(data['password'])

        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')  
        user_type = validated_data.get('user_type')
        if user_type == 'admin':
            user = User.objects.create_superuser(**validated_data)
        else:
            user = User.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate_email(self, value):
        # Ensure the email format is correct
        EmailValidator()(value)
        return value

    def validate(self, data):
        if not data.get('email') or not data.get('password'):
            raise serializers.ValidationError("Both email and password are required.")
        return data
