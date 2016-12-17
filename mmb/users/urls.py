from django.conf.urls import patterns, url, include
from rest_framework import routers

from users.views import UserProfileViewset, UserViewset, UserFollowerViewset,\
    UserCreateViewset, PasswordChangeView, activate_user, get_user_instrument

router = routers.DefaultRouter()
router.register(r'profile', UserProfileViewset)
router.register(r'user', UserViewset)
router.register(r'follow', UserFollowerViewset)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^thumbnail-details/$', UserProfileViewset.as_view({"get": "user_thumbnail_details"})),
    url(r'^get-profile/$', UserProfileViewset.as_view({"get": "get_profile"})),
    url(r'^validate/username/(?P<username>.*)\/$', UserViewset.as_view({"get": "validate_username"})),
    url(r'^auth-details/$', UserViewset.as_view({"get": "auth_details"})),
    url(r'^update-pic/$', UserViewset.as_view({"put": "update_profile_pic"})),
    url(r'^create/$', UserCreateViewset.as_view({"post": "create"})),
    url(r'^password/change/$', PasswordChangeView.as_view(), name='password_change'),
    url(r'^activate/(?P<key>.+)$', activate_user),
    url(r'^ins/(?P<user_id>.+)$', get_user_instrument)
]

