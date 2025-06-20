from rest_framework import serializers
from orders.models import Order, OrderItem
from products.serializers import ProductSerializer
from core.serializers.accounts import UserAccountSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = "__all__"

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["product"] = ProductSerializer(
            instance.product, context={"request": self.context.get("request")}
        ).data
        return data


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["customer"] = UserAccountSerializer(
            instance.customer, context={"request": self.context.get("request")}
        ).data
        data["order_items"] = OrderItemSerializer(
            instance.order_items(),
            many=True,
            context={"request": self.context.get("request")},
        ).data
        if instance.sales_person:
            data["sales_person"] = UserAccountSerializer(
                instance.sales_person, context={"request": self.context.get("request")}
            ).data
        else:
            data["sales_person"] = None

        data["payment_status"] = instance.payment_status
        return data
