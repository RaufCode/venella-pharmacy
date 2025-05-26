from rest_framework import serializers
from carts.models import Cart, CartItem
from products.serializers import ProductSerializer
from core.serializers.accounts import UserAccountSerializer


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = "__all__"

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["product"] = ProductSerializer(instance.product).data
        return data


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = "__all__"

    def validate(self, attrs):
        if attrs["quantity"] <= 0:
            raise serializers.ValidationError("Quantity must be greater than zero.")

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["customer"] = UserAccountSerializer(instance.customer).data
        data["items"] = CartItemSerializer(instance.items.all(), many=True).data
        return data
