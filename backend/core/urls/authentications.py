from django.urls import path
from core.views.authentications import SignInView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)


AUTH_URLS = [
    path("auth/login/", SignInView.as_view()),
    path("auth/token/", TokenObtainPairView.as_view()),
    path("auth/token/refresh/", TokenRefreshView.as_view()),
    path("auth/token/verify/", TokenVerifyView.as_view()),
]
