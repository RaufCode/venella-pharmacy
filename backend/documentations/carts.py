from ._base import *
from carts.serializers import CartItemSerializer

list_all_cart_items_schema = extend_schema(
    summary="List All Cart Items",
    description="This retrieves all cart items in the system.",
    responses={
        200: CartItemSerializer(many=True),
    },
    tags=["Carts"],
)

list_customer_cart_items_schema = extend_schema(
    summary="List Customer Cart Items",
    description="This retrieves all cart items for a specific customer.",
    responses={200: CartItemSerializer(many=True)},
)

add_cart_item_schema = extend_schema(
    summary="Add Cart Item",
    description="This adds a new item to the customer's cart.",
    request=CartItemSerializer,
    responses={
        201: inline_serializer(
            name="AddCartItemResponse",
            fields={"detail": serializers.CharField(), "item": CartItemSerializer()},
        ),
    },
    tags=["Carts"],
)

update_cart_item_schema = extend_schema(
    summary="Update Cart Item",
    description="This updates an existing item in the customer's cart.",
    request=CartItemSerializer,
    responses={
        200: inline_serializer(
            name="UpdateCartItemResponse",
            fields={"detail": serializers.CharField(), "item": CartItemSerializer()},
        ),
    },
    tags=["Carts"],
)

delete_cart_item_schema = extend_schema(
    summary="Delete Cart Item",
    description="This deletes an item from the customer's cart.",
    responses={
        204: inline_serializer(
            name="DeleteCartItemResponse", fields={"detail": serializers.CharField()}
        ),
    },
    tags=["Carts"],
)
