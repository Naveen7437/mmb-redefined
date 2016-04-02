from django.conf.urls import patterns, url, include
from rest_framework import routers
router = routers.SimpleRouter()

from users.views import UserProfileViewset, UserViewset


router = routers.DefaultRouter()
router.register(r'profile', UserProfileViewset)
router.register(r'user', UserViewset)

urlpatterns = [
    url(r'^', include(router.urls)),
]