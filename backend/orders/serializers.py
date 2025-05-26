from rest_framework import serializers
from orders.models import Order, OrderItems
from products.serializers import ProductSerializer
from core.serializers.accounts import UserAccountSerializer


class OrderItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItems
        fields = "__all__"

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["product"] = ProductSerializer(instance.product).data


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["customer"] = UserAccountSerializer(instance.customer).data
        data["order_items"] = OrderItemsSerializer(
            instance.order_items.all(), many=True
        ).data
        return data
