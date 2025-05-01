from rest_framework import serializers
from .models import Product, ProductCategory, ProductImage


class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = "__all__"


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"

    def validate(self, data):
        if data["stock"] < 0:
            raise serializers.ValidationError("Stock cannot be negative.")
        return data

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["category"] = ProductCategorySerializer(instance.category).data
        data["images"] = ProductImageSerializer(instance.images.all(), many=True).data
        return data
