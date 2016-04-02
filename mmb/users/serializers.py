import validators
from rest_framework import serializers
from django.contrib.auth import get_user_model

from users.models import Profile, User


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
