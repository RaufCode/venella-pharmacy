from ._base import *
from carts.serializers import CartItemSerializer, CartSerializer

list_all_cart_items_schema = extend_schema(
    summary="List All Cart Items",
    description="This retrieves all cart items in the system.",
    responses={
        200: CartItemSerializer(many=True),
    },
    tags=["Carts"],
)

retrieve_cart_item_schema = extend_schema(
    summary="Retrieve Cart Item",
    description="This retrieves a specific cart item by its ID.",
    responses={
        200: CartItemSerializer(),
    },
    tags=["Carts"],
)

list_customer_cart_items_schema = extend_schema(
    summary="List Customer Cart Items",
    description="This retrieves all cart items for a specific customer.",
    responses={200: CartItemSerializer(many=True)},
    tags=["Carts"],
)

add_cart_item_schema = extend_schema(
    summary="Add Cart Item",
    description="This adds a new item to the customer's cart.",
    request=inline_serializer(
        name="AddCartItemRequest",
        fields={
            "product": serializers.UUIDField(help_text="ID of the product to add"),
            "quantity": serializers.IntegerField(
                default=1, help_text="Quantity of the product to add"
            ),
        },
    ),
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
    request=inline_serializer(
        name="UpdateCartItemRequest",
        fields={
            "quantity": serializers.IntegerField(
                default=1, help_text="New quantity of the product"
            ),
        },
    ),
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


list_carts_schema = extend_schema(
    summary="List All Carts",
    description="This retrieves all carts in the system.",
    responses={
        200: CartItemSerializer(many=True),
    },
    tags=["Carts"],
)

retrieve_cart_schema = extend_schema(
    summary="Retrieve Cart",
    description="This retrieves all items in a specific cart.",
    responses={
        200: CartSerializer(many=True),
    },
    tags=["Carts"],
)
