from ._base import *
from orders.serializers import OrderSerializer


list_orders_schema = extend_schema(
    description="List all orders",
    responses={
        200: OrderSerializer(many=True),
    },
)

retrieve_order_schema = extend_schema(
    description="Retrieve a specific order by ID",
    responses={
        200: OrderSerializer(many=False),
    },
)

list_customer_orders_schema = extend_schema(
    description="List all orders for the authenticated customer",
    responses={
        200: OrderSerializer(many=True),
    },
)

create_order_schema = extend_schema(
    description="Create a new order for the authenticated customer",
    request=inline_serializer(
        name="CreateOrderRequest",
        fields={
            "total_amount": serializers.DecimalField(max_digits=10, decimal_places=2),
            "shipping_address": serializers.CharField(max_length=255),
            "order_items": serializers.ListField(
                child=inline_serializer(
                    name="OrderItem",
                    fields={
                        "product": serializers.UUIDField(),
                        "quantity": serializers.IntegerField(min_value=1),
                        "amount": serializers.DecimalField(
                            max_digits=10, decimal_places=2
                        ),
                    },
                ),
                min_length=1,
            ),
        },
        required=["total_amount", "shipping_address", "order_items"],
    ),
    responses={
        201: OrderSerializer(many=False),
    },
)
