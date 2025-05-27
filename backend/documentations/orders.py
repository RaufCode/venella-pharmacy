from ._base import *
from orders.serializers import OrderSerializer


list_orders_schema = extend_schema(
    description="List all orders",
    responses={
        200: OrderSerializer(many=True),
    },
    tags=["Orders"],
)

retrieve_order_schema = extend_schema(
    description="Retrieve a specific order by ID",
    responses={
        200: OrderSerializer(many=False),
    },
    tags=["Orders"],
)

list_customer_orders_schema = extend_schema(
    description="List all orders for the authenticated customer",
    responses={
        200: OrderSerializer(many=True),
    },
    tags=["Orders"],
)

create_order_schema = extend_schema(
    description="Create a new order for the authenticated customer",
    request=inline_serializer(
        name="CreateOrderRequest",
        fields={
            "cart": serializers.UUIDField(),
            "shipping_address": serializers.CharField(max_length=255),
        },
        required=["cart", "shipping_address"],
    ),
    responses={
        201: OrderSerializer(many=False),
    },
    tags=["Orders"],
)
