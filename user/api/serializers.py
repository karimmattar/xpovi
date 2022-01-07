import re

from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.core.validators import validate_email
from rest_framework import serializers

from .utills import generate_access_token, generate_refresh_token

User = get_user_model()


class LoginSerializer(serializers.Serializer):  # Login serializer takes [email, password]
    email = serializers.EmailField(required=True, validators=[validate_email])
    password = serializers.CharField(min_length=8, required=True)

    @property
    def clean_user(self):
        try:
            user = User.objects.get(email=self.validated_data['email'])
        except ObjectDoesNotExist:
            raise serializers.ValidationError({'code': 404, 'message': 'use not found'})

        if not user.check_password(self.validated_data['password']):
            raise serializers.ValidationError({'code': 403, 'message': 'wrong password'})

        access_token = generate_access_token(user)
        refresh_token = generate_refresh_token(user)

        return access_token, refresh_token


class RegisterSerializer(serializers.ModelSerializer):  # Register serializer takes[email, username, fname, lname, pass1, pass2]
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    def validate(self, data):
        password1 = data.get('password1')
        password2 = data.get('password2')
        # Password regex validator at least 8 chars includes 1 alphabetic and 1 digit at least.
        pattern = '^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$'
        result = re.findall(pattern, password1)
        if not result:
            raise serializers.ValidationError('Password must contain at least 8 characters, 1 digit and 1 char')
        if password2 != password1:
            raise serializers.ValidationError('Passwords do not match.')
        return data

    def create(self, validated_data):
        password1 = validated_data.pop('password1')
        password2 = validated_data.pop('password2')
        user = User(**validated_data)
        user.save()
        user.set_password(password1)
        user.save()
        return user

    class Meta:
        model = User
        fields = [
            'email', 'username', 'first_name', 'last_name', 'password1', 'password2'
        ]
