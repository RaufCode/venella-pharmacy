from notifications.models import (
    Notification,
    CustomerNotification,
    SalesPersonNotification,
)
from rest_framework import serializers
from core.serializers.accounts import UserAccountSerializer


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model= Notification
        fields = "__all__"

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["type"] = instance.type_display
        return data


class CustomerNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerNotification
        fields = "__all__"

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["customer"] = UserAccountSerializer(
            instance.customer, context={"request": self.context.get("request")}
        ).data
        data["type"] = instance.type_display
        return data


class SalesPersonNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesPersonNotification
        fields = "__all__"

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["type"] = instance.type_display
        return data
