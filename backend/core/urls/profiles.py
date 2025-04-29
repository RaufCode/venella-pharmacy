from django.urls import path
from core.views.profiles import ProfileViewSet

PROFILES_URLS = [
    path("profiles/", ProfileViewSet.as_view({"get": "list"})),
    path(
        "profiles/<str:profile_id>/retrieve/",
        ProfileViewSet.as_view({"get": "retrieve"}),
    ),
    path(
        "profiles/<str:profile_id>/update/", ProfileViewSet.as_view({"put": "update"})
    ),
    path(
        "profiles/<str:profile_id>/delete/",
        ProfileViewSet.as_view({"delete": "destroy"}),
    ),
]
