import validators
from rest_framework import serializers
from django.contrib.auth import get_user_model

from users.models import Profile, User, UserFollower
from mdata.serializers import GenreSerializer,  InstrumentSerializer


class UserProfileCreateSerializer(serializers.ModelSerializer):
    """
    serializer to create and update user profile
    """

    class Meta:
        model = Profile


class UserProfileSerializer(serializers.ModelSerializer):
    """
    serializes the user profile data
    """
    username = serializers.CharField(source='user.username', required=False, read_only=True)
    full_name = serializers.CharField(source='user.get_full_name', required=False, read_only=True)
    avatar = serializers.SerializerMethodField("get_avatar_url")
    genre = GenreSerializer(many=True, read_only=True)
    instrument = InstrumentSerializer(many=True, read_only=True)

    def get_avatar_url(self, obj):
        """
        return absolute url of avatar
        """
        url = ''
        if obj.user.avatar:
            url = self.context.get('request').build_absolute_uri(obj.user.avatar.url)
        return url

    class Meta:
        model = Profile


class UserSerializer(serializers.ModelSerializer):
    """
    returns basic user details
    """

    class Meta:
        model = User

        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'avatar')


# Todo: temporary solution, to be removed
class UserAuthDetailsSerializer(serializers.ModelSerializer):
    """

    """
    is_new = serializers.SerializerMethodField('check_new_user')
    avatar = serializers.SerializerMethodField("get_avatar_url")

    def get_avatar_url(self, obj):
        """
        return absolute url of avatar
        """
        url = ''
        if obj.user.avatar:
            url = self.context.get('request').build_absolute_uri(obj.user.avatar.url)
        return url

    def check_new_user(self, obj):
        """
        return True if user profile does not exist
        """
        request = self.context.get('request')
        user = request.user

        try:
            Profile.objects.get(user=user)
        except (Profile.DoesNotExist, TypeError):
            return True
        return False

    class Meta:
        model = User

        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'is_new', 'avatar')


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


