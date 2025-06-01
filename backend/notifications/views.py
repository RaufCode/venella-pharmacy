from rest_framework import viewsets, status
from rest_framework.response import Response
from notifications.selectors import *
from documentations.notifications import *


class NotificationViewSet(viewsets.ViewSet):

    @all_notifications_schema
    def all_notifications(self, request):
        notifications = get_all_notifications()
        context = notification_representation(request, notifications, many=True)
        return Response(context, status=status.HTTP_200_OK)

    @sales_person_notifications_schema
    def sales_person_notifications(self, request):
        notifications = get_notifications_by_types(
            ["NEW_ORDER", "PRODUCT_STOCK_ALERT", "SYSTEM_ALERT"]
        )
        context = notification_representation(request, notifications, many=True)
        return Response(context, status=status.HTTP_200_OK)

    @mark_as_read_schema
    def mark_as_read(self, request, notification_id):
        notification = get_notification_by_id(notification_id)
        if not notification:
            return Response(
                {"detail": "Notification not found"}, status=status.HTTP_404_NOT_FOUND
            )

        notification.read = True
        notification.save()

        context = notification_representation(request, notification)
        return Response(context, status=status.HTTP_200_OK)
