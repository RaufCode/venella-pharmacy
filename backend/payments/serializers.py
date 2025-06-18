from rest_framework import serializers
from .models import Payment, PaymentMethod
from orders.serializers import OrderSerializer


class PaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = ["id", "method_type", "details"]
        read_only_fields = ["id"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        return data


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = [
            "id",
            "order",
            "payment_method",
            "amount",
            "currency",
            "status",
            "created_at",
            "updated_at",
            "transaction_id",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["order"] = OrderSerializer(
            instance.order, context={"request": self.context.get("request")}
        ).data
        if instance.payment_method:
            data["payment_method"] = PaymentMethodSerializer(
                instance.payment_method,
                context={"request": self.context.get("request")},
            ).data
        else:
            data["payment_method"] = None
        return data
