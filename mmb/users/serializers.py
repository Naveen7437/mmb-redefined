from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm

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
    is_follower = serializers.SerializerMethodField('followed_by_user')

    def get_avatar_url(self, obj):
        """
        return absolute url of avatar
        """
        url = ''
        if obj.user.avatar:
            url = self.context.get('request').build_absolute_uri(obj.user.avatar.url)
        return url

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
            user_follower = UserFollower.objects.get(follower=user, following=obj.user)
        except UserFollower.DoesNotExist:
            return None

        return user_follower.id

    class Meta:
        model = Profile

class UserSerializer(serializers.ModelSerializer):
    """
    returns basic user details
    """

    class Meta:
        model = User

        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'avatar', 'gender')


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
        if obj.avatar:
            url = self.context.get('request').build_absolute_uri(obj.avatar.url)
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


class UserFollowerSerializer(serializers.ModelSerializer):
    """

    """
    class Meta:
        model = UserFollower


class UserCreateSerializer(serializers.ModelSerializer):
    """

    """
    email = serializers.CharField(required=True)
    username = serializers.CharField(required=True)

    class Meta:
        model = get_user_model()
        fields = (
            'id',
            'username',
            'password',
            'email'
        )
        extra_kwargs = {
            'password': {'write_only': True},
        }


class PasswordChangeSerializer(serializers.Serializer):
    """
    password change of user
    """

    old_password = serializers.CharField(max_length=128)
    new_password1 = serializers.CharField(max_length=128)
    new_password2 = serializers.CharField(max_length=128)

    set_password_form_class = SetPasswordForm

    def __init__(self, *args, **kwargs):

        super(PasswordChangeSerializer, self).__init__(*args, **kwargs)

        self.request = self.context.get('request')
        self.user = getattr(self.request, 'user', None)

    def validate_old_password(self, value):
        invalid_password_conditions = (
            self.user,
            not self.user.check_password(value)
        )

        if all(invalid_password_conditions):
            raise serializers.ValidationError('Invalid password')
        return value

    def validate(self, attrs):
        self.set_password_form = self.set_password_form_class(
            user=self.user, data=attrs
        )

        if not self.set_password_form.is_valid():
            raise serializers.ValidationError(self.set_password_form.errors)
        return attrs

    def save(self):
        self.set_password_form.save()

