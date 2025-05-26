from ._base import *
from products.serializers import (
    ProductSerializer,
    ProductCategorySerializer,
    ProductImageSerializer,
)


list_products_schema = extend_schema(
    summary="List Products",
    description="This endpoint retrieves a list of all products in the system.",
    request=ProductSerializer,
    responses={
        200: ProductSerializer(many=True),
    },
    tags=["Products"],
)

retrieve_product_schema = extend_schema(
    summary="Retrieve Product",
    description="This endpoint retrieves a specific product by its ID.",
    request=ProductSerializer,
    responses={
        200: ProductSerializer(),
    },
    tags=["Products"],
)

create_products_schema = extend_schema(
    summary="Create Products",
    description="This endpoint creates a new product in the system.",
    request=inline_serializer(
        name="CreateProductsRequest",
        fields={
            "name": serializers.CharField(),
            "description": serializers.CharField(),
            "price": serializers.DecimalField(max_digits=10, decimal_places=2),
            "stock": serializers.IntegerField(),
            "category": serializers.UUIDField(),
            "product_images": serializers.ListField(
                child=serializers.DictField(
                    child=serializers.ImageField(), required=False
                ),
                required=False,
            ),
        },
    ),
    responses={
        200: ProductSerializer(),
    },
    tags=["Products"],
)

update_product_schema = extend_schema(
    summary="Update Product",
    description="This endpoint updates an existing product.",
    request=inline_serializer(
        name="UpdateProductRequest",
        fields={
            "name": serializers.CharField(required=False),
            "description": serializers.CharField(required=False),
            "price": serializers.DecimalField(
                max_digits=10, decimal_places=2, required=False
            ),
            "stock": serializers.IntegerField(required=False),
            "category": serializers.UUIDField(required=False),
            "product_images": serializers.ListField(
                child=serializers.DictField(
                    child=serializers.ImageField(),
                    required=False,
                ),
                required=False,
            ),
        },
    ),
    responses={
        200: ProductSerializer(),
    },
    tags=["Products"],
)

delete_product_schema = extend_schema(
    summary="Delete Product",
    description="This endpoint deletes a specific product by its ID.",
    responses={
        204: None,
    },
    tags=["Products"],
)

search_products_schema = extend_schema(
    summary="Search Products",
    description="This endpoint searches for products based on a query string.",
    parameters=[
        OpenApiParameter(
            name="query",
            description="Search query string to filter products by name.",
            location=OpenApiParameter.QUERY,
            type=OpenApiTypes.STR,
            required=False,
        ),
    ],
    request=ProductSerializer,
    responses={
        200: ProductSerializer(many=True),
    },
    tags=["Products"],
)


list_categories_schema = extend_schema(
    summary="List Product Categories",
    description="This endpoint retrieves a list of all product categories.",
    request=ProductCategorySerializer,
    responses={
        200: ProductCategorySerializer(many=True),
    },
    tags=["Product Categories"],
)

retrieve_category_schema = extend_schema(
    summary="Retrieve Product Category",
    description="This endpoint retrieves a specific product category by its ID.",
    request=ProductCategorySerializer,
    responses={
        200: ProductCategorySerializer(),
    },
    tags=["Product Categories"],
)

create_category_schema = extend_schema(
    summary="Create Product Category",
    description="This endpoint creates a new product category.",
    request=ProductCategorySerializer,
    responses={
        201: ProductCategorySerializer(),
    },
    tags=["Product Categories"],
)

update_category_schema = extend_schema(
    summary="Update Product Category",
    description="This endpoint updates an existing product category.",
    request=ProductCategorySerializer,
    responses={
        200: ProductCategorySerializer(),
    },
    tags=["Product Categories"],
)

delete_category_schema = extend_schema(
    summary="Delete Product Category",
    description="This endpoint deletes a specific product category by its ID.",
    responses={
        204: None,
    },
    tags=["Product Categories"],
)
