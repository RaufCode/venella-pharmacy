from django.urls import path
from core.views.authentications import SignInView, PasswordViewSet
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from drf_spectacular.utils import extend_schema, extend_schema_view


AUTH_URLS = [
    path("auth/login/", SignInView.as_view()),
    path(
        "auth/token/",
        extend_schema_view(
            post=extend_schema(summary="Obtain Tokens", tags=["Tokens"])
        )(TokenObtainPairView.as_view()),
    ),
    path(
        "auth/token/refresh/",
        extend_schema_view(
            post=extend_schema(summary="Refresh Tokens", tags=["Tokens"])
        )(TokenRefreshView.as_view()),
    ),
    path(
        "auth/token/verify/",
        extend_schema_view(
            post=extend_schema(summary="Verify Tokens", tags=["Tokens"])
        )(TokenVerifyView.as_view()),
    ),
    path(
        "auth/password/change/<str:user_id>/",
        PasswordViewSet.as_view({"post": "change_password"}),
    ),
]
