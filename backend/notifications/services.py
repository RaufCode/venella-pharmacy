from notifications.models import (
    Notification,
    SalesPersonNotification,
    CustomerNotification,
)
from notifications.serializers import (
    SalesPersonNotificationSerializer,
    CustomerNotificationSerializer,
)


def create_salesperson_notification(data: dict):
    serializer = SalesPersonNotificationSerializer(data=data)
    if serializer.is_valid():
        notification = serializer.save()
        return notification, None
    return None, serializer.errors


def create_customer_notification(data: dict):
    serializer = CustomerNotificationSerializer(data=data)
    if serializer.is_valid():
        notification = serializer.save()
        return notification, None
    return None, serializer.errors
