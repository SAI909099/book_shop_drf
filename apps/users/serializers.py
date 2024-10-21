from django.conf import settings
from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.fields import CharField, EmailField
from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from datetime import timedelta
from users.models import User
from django.contrib.auth.hashers import make_password
import redis
from urllib.parse import urlparse

redis_url = urlparse(settings.CELERY_BROKER_URL)

r = redis.StrictRedis(host=redis_url.hostname, port=redis_url.port, db=int(redis_url.path.lstrip('/')))

class UserModelSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class UserWishlist(ModelSerializer):
    class Meta:
        model = User
        fields = 'wishlist',


class UserUpdateSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'email']


class RegisterUserModelSerializer(ModelSerializer):
    confirm_password = CharField(write_only=True)

    class Meta:
        model = User
        fields = 'id', 'email', 'password', 'confirm_password', 'first_name',

        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, attrs):
        confirm_password = attrs.pop('confirm_password')
        if confirm_password != attrs.get('password'):
            raise ValidationError('Passwords did not match!')
        attrs['password'] = make_password(confirm_password)
        return attrs


class LoginUserModelSerializer(Serializer):
    email = EmailField()
    password = CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
#todo shettan o'zgartirdim

        redis_key = f'failed_attempts_{email}'
        attempts = r.get(redis_key)
        if attempts and int(attempts) >= 5:
            raise ValidationError("Too many failed login attempts. Try again after 5 minutes.")

        user = authenticate(username=email, password=password)

        if user is None:
            # If the user fails to authenticate, increase the count of failed attempts
            current_attempts = int(attempts) if attempts else 0
            r.setex(redis_key, timedelta(minutes=5), current_attempts + 1)  # Block for 5 minutes
            raise ValidationError("Invalid email or password")

            # If authentication is successful, reset the attempt counter
        r.delete(redis_key)
        attrs['user'] = user
        return attrs


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        return token