from django.conf.urls import patterns, url, include
from rest_framework import routers
router = routers.SimpleRouter()

from users.views import UserProfileViewset, UserViewset


router = routers.DefaultRouter()
router.register(r'profile', UserProfileViewset)
router.register(r'user', UserViewset)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^thumbnail-details/$', UserProfileViewset.as_view({"get": "user_thumbnail_details"})),
    url(r'^validate/username/(?P<username>.*)\/$', UserViewset.as_view({"get": "validate_username"})),
    url(r'^auth-details/$', UserViewset.as_view({"get": "auth_details"}))
]

