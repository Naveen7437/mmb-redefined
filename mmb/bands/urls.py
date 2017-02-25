from django.conf.urls import patterns, url, include
from rest_framework import routers

from bands.views import BandVacancyViewset, \
    BandViewset, BandFollowersViewset, UserBandMemberViewset,\
    BandMemberFetch, BandMemberCreate, BandMemberUpdate,\
    BandUserInviteViewset, BandVacancyApplicationViewset, BandVacancyFetchViewset



router = routers.DefaultRouter()
router.register(r'band', BandViewset)
router.register(r'vacancy', BandVacancyViewset)
router.register(r'follower', BandFollowersViewset)
# router.register(r'member', BandMemberViewset)
router.register(r'user', UserBandMemberViewset)
router.register(r'invite', BandUserInviteViewset)
router.register(r'vacancy-app', BandVacancyApplicationViewset)

urlpatterns = [
    url(r'^', include(router.urls)),
    # url(r'^invite/$', BandMemberViewset.as_view({"get": "invite"})),
    url(r'^member/fetch/$', BandMemberFetch.as_view()),
    url(r'^member/create/$', BandMemberCreate.as_view()),
    url(r'^member/update/(?P<pk>[0-9]+)/$', BandMemberUpdate.as_view()),
    url(r'^vacancy-fetch/$', BandVacancyFetchViewset.as_view()),
]

