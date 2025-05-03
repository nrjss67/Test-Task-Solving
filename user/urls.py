from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView,
)
from rest_framework import routers

from user.views import UserCreateView, ProfileView


router = routers.DefaultRouter()
router.register(r"profile", ProfileView, basename="profile")


urlpatterns = [
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/blacklist/", TokenBlacklistView.as_view(), name="token_blacklist"),
    path("signup/", UserCreateView.as_view(), name="signup"),
    path("", include(router.urls)),
]
