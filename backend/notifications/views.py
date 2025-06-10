from rest_framework import viewsets, status
from rest_framework.response import Response
from notifications.selectors import *
from documentations.notifications import *
from core.selectors.accounts import get_user_account_by_id


class NotificationViewSet(viewsets.ViewSet):

    # @all_notifications_schema
    # def all_notifications(self, request):
    #     notifications = get_all_notifications()
    #     context = notification_representation(request, notifications, many=True)
    #     return Response(context, status=status.HTTP_200_OK)

    @sales_person_notifications_schema
    def sales_person_notifications(self, request):
        notifications = get_salesperson_notifications()
        context = salesperson_notification_representation(
            request, notifications, many=True
        )
        return Response(context, status=status.HTTP_200_OK)

    @customer_notifications_schema
    def customer_notifications(self, request, custoer_id):
        customer = get_user_account_by_id(custoer_id)
        if not customer:
            return Response(
                {"detail": "Customer not found"}, status=status.HTTP_404_NOT_FOUND
            )
        notifications = get_customer_notifications(customer_id=custoer_id)
        context = customer_notification_representation(
            request, notifications, many=True
        )
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

        context = (
            customer_notification_representation(request, notification)
            if hasattr(notification, "customer")
            else salesperson_notification_representation(request, notification)
        )
        return Response(context, status=status.HTTP_200_OK)
