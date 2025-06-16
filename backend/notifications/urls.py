from django.urls import path
from notifications.views import NotificationViewSet

urlpatterns = [
    # path("", NotificationViewSet.as_view({"get": "all_notifications"})),
    path(
        "sales-person/",
        NotificationViewSet.as_view({"get": "sales_person_notifications"}),
    ),
    path(
        "customer/<str:custoer_id>/",
        NotificationViewSet.as_view({"get": "customer_notifications"}),
    ),
    path(
        "<str:notification_id>/mark-as-read/",
        NotificationViewSet.as_view({"put": "mark_as_read"}),
    ),
    path(
        "<str:notification_id>/delete/",
        NotificationViewSet.as_view({"delete": "delete_notification"}),
    ),
]
