from django.http import HttpRequest
from notifications.models import (
    Notification,
    CustomerNotification,
    SalesPersonNotification,
)
from notifications.serializers import (
    NotificationSerializer,
    CustomerNotificationSerializer,
    SalesPersonNotificationSerializer,
)


def get_all_notifications():
    return Notification.objects.all()


def get_notification_by_id(notification_id: str):
    try:
        notification = Notification.objects.get(id=notification_id)
        return notification
    except Notification.DoesNotExist:
        return None

def get_customer_notification_by_id(customer_notification_id: str):
    try:
        customer_notification = CustomerNotification.objects.get(id=customer_notification_id)
        return customer_notification
    except CustomerNotification.DoesNotExist:
        return None


def get_customer_notifications(customer_id: str):
    notifications = CustomerNotification.objects.filter(customer=customer_id)
    return notifications


def get_notifications_by_types(notification_types: list):
    notifications = Notification.objects.filter(type__in=notification_types)
    return notifications


def get_salesperson_notifications():
    notifications = SalesPersonNotification.objects.all()
    return notifications


def salesperson_notification_representation(
    request: HttpRequest, salesperson_notification: SalesPersonNotification, many: bool
):
    serializer = SalesPersonNotificationSerializer(
        salesperson_notification, many=many, context={"request": request}
    )
    return serializer.data


def customer_notification_representation(request: HttpRequest, customer_notification: CustomerNotification, many: bool = False):
    serializer = CustomerNotificationSerializer(customer_notification, many=many, context={'request': request})
    return serializer.data
