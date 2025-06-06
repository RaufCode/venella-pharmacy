from ._base import *
from notifications.serializers import NotificationSerializer


all_notifications_schema = extend_schema(
    summary="List notification",
    description="This retrieves all notifications in the system.",
    responses={
        200: NotificationSerializer(many=True),
    },
    tags=["Notifications"],
)

sales_person_notifications_schema = extend_schema(
    summary="Notifications for Sales Person",
    description="This retrieves notifications a sales person.",
    responses={
        200: NotificationSerializer(many=True),
    },
    tags=["Notifications"],
)

mark_as_read_schema = extend_schema(
    summary="Mark Notification as Read",
    description="Marks a specific notification as read.",
    request=None,
    responses={
        200: NotificationSerializer(),
    },
    tags=["Notifications"],
)
