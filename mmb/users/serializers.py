import validators
from rest_framework import serializers
from django.contrib.auth import get_user_model

from users.models import Profile, User, UserFollower


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


class UserDetailSerializer(serializers.ModelSerializer):
    """
    serializes the thumbnail details of a user
    """
    user_name = serializers.CharField(source='username', required=False, read_only=True)
    first_name = serializers.CharField(source='firstname', required=False, read_only=True)
    last_name = serializers.CharField(source='lastname', required=False, read_only=True)
    is_follower = serializers.SerializerMethodField('followed_by_user')

    def followed_by_user(self, obj):
        """

        :param obj:
        :return:
        """
        request = self.context.get('request')
        user = request.user
        if user.is_anonymous():
            return None

        try:
            UserFollower.objects.get(follower=user, following=obj.user)
        except UserFollower.DoesNotExist:
            return False

        return True


    class Meta:
        model = Profile

        fields = ('user_name', 'first_name', 'last_name', 'instrument',
                  'followed_by_count', 'is_follower')


