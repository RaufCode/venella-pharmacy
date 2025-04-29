from django.urls import path
from core.views.accounts import UserAccountViewset

ACCOUNTS_URLS = [
    path("accounts/", UserAccountViewset.as_view({"get": "list"})),
    path("accounts/create/", UserAccountViewset.as_view({"post": "create"})),
    path(
        "accounts/<str:user_id>/retrieve/",
        UserAccountViewset.as_view({"get": "retrieve"}),
    ),
    path(
        "accounts/<str:user_id>/update/",
        UserAccountViewset.as_view({"put": "update"}),
    ),
    path(
        "accounts/<str:user_id>/delete/",
        UserAccountViewset.as_view({"delete": "destroy"}),
    ),
]
