from django.conf.urls import patterns, url, include
from rest_framework import routers
router = routers.SimpleRouter()

from bands.views import BandMemberViewset, BandVacancyViewset, \
    BandViewset, BandFollowersViewset


router = routers.DefaultRouter()
router.register(r'band', BandViewset)
router.register(r'vacancy', BandVacancyViewset)
router.register(r'follower', BandFollowersViewset)
router.register(r'member', BandMemberViewset)


urlpatterns = [
    url(r'^', include(router.urls))
]

