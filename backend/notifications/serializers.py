from notifications.models import Notification, CustomerNotification
from rest_framework import serializers
from core.serializers.accounts import UserAccountSerializer


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model= Notification
        fields = "__all__"


    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['type'] = instance.get_type_display()
        return data
    

class CustomerNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerNotification
        fields = "__all__"


    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['notification'] = NotificationSerializer(instance.notification, context={'request': self.context.get('request')}).data
        data['customer'] = UserAccountSerializer(instance.user, context={'request': self.context.get('request')}).data
        return data