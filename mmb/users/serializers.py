import validators
from rest_framework import serializers
from django.contrib.auth import get_user_model

from users.models import Profile, User


class UserProfileSerializer(serializers.ModelSerializer):
    """
    serializes the user profile data
    """
    user_name = serializers.CharField(source='username', required=False, read_only=True)
    first_name = serializers.CharField(source='firstname', required=False, read_only=True)
    last_name = serializers.CharField(source='lastname', required=False, read_only=True)

    class Meta:
        model = Profile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
