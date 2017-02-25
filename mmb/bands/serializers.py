from django.contrib.auth import get_user_model
from rest_framework import serializers


from bands.models import Band, BandFollowers, BandMember,\
    BandVacancy, BandVacancyApplication, BandUserInvite
from mdata.serializers import InstrumentSerializer
from users.serializers import UserMemberSerializer


class BandSerializer(serializers.ModelSerializer):
    """

    """
    class Meta:
        model = Band

    def create(self, validated_data):
        # TODO: need rework
        obj = Band()
        obj.lable  = validated_data.get('label')
        obj.location  = validated_data.get('location')
        obj.year  = validated_data.get('year')
        obj.name  = validated_data.get('name')
        obj.desc  = validated_data.get('desc')
        # obj.genre = validated_data.get('genre')
        user = self.context.get('request').user
        if user.is_anonymous():
            obj.created_by = get_user_model().objects.get(username="admin")
        else:
            obj.created_by = user

        obj.save()
        for genre in validated_data.get('genre'):
            obj.genre.add(genre)

        return obj


class BandVacancySerializer(serializers.ModelSerializer):
    """

    """
    class Meta:
        model = BandVacancy


class BandVacancyFetchSerializer(serializers.ModelSerializer):

    is_applied = serializers.SerializerMethodField('applied_by_user')

    def applied_by_user(self, obj):
        request = self.context.get('request')
        user = request.user
        if user.is_anonymous():
            return None

        try:
            BandVacancyApplication.objects.get(band_vacancy=obj,
                                               applicant=user, active=True)
        except BandVacancyApplication.DoesNotExist:
            return False

        return True

    class Meta:
        model = BandVacancy



class BandMemberCreateSerializer(serializers.ModelSerializer):
    """

    """
    class Meta:
        model = BandMember

class BandFollowersSerializer(serializers.ModelSerializer):
    """

    """
    class Meta:
        model = BandFollowers


class BandMemberSerializer(serializers.ModelSerializer):
    """

    """
    instrument = InstrumentSerializer()
    member = UserMemberSerializer()

    class Meta:
        model = BandMember




class UserBandSerializer(serializers.ModelSerializer):
    """

    """
    image = serializers.SerializerMethodField("get_image_url")

    def get_image_url(self, obj):
        """
        return absolute url of image
        """
        url = ''
        if obj.image:
            url = self.context.get('request').build_absolute_uri(obj.image.url)
        return url


    class Meta:
        model = Band
        fields = ('id', 'name', 'image')


class UserBandMemberSerializer(serializers.ModelSerializer):
    """

    """
    band = UserBandSerializer(read_only=True)

    class Meta:
        model = BandMember
        fields = ('band', 'member')


class BandVacancyApplicationSerializer(serializers.ModelSerializer):
    """

    """
    class Meta:
        model = BandVacancyApplication


class BandUserInviteSerializer(serializers.ModelSerializer):
    """

    """
    class Meta:
        model = BandUserInvite












