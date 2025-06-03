from django.urls import path
from notifications.views import NotificationViewSet

urlpatterns = [
    path("", NotificationViewSet.as_view({"get": "all_notifications"})),
    path(
        "sales-person/",
        NotificationViewSet.as_view({"get": "sales_person_notifications"}),
    ),
    path(
        "<str:notification_id>/mark-as-read/",
        NotificationViewSet.as_view({"put": "mark_as_read"}),
    ),
]
