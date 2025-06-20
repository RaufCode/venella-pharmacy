from ._base import *
from orders.serializers import OrderSerializer
from payments.serializers import PaymentSerializer


list_orders_schema = extend_schema(
    summary="List all orders in DB",
    description="List all orders in the system",
    responses={
        200: OrderSerializer(many=True),
    },
    tags=["Orders"],
)

retrieve_order_schema = extend_schema(
    summary="Retrieve an order",
    description="Retrieve a specific order by ID",
    responses={
        200: OrderSerializer(many=False),
    },
    tags=["Orders"],
)

list_customer_orders_schema = extend_schema(
    summary="List a customer's orders",
    description="List all orders for the authenticated customer",
    responses={
        200: OrderSerializer(many=True),
    },
    tags=["Orders"],
)

create_order_schema = extend_schema(
    summary="Create an order by customer",
    description="Create a new order for the authenticated customer",
    request=inline_serializer(
        name="CreateOrderRequest",
        fields={
            "cart": serializers.UUIDField(),
            "shipping_address": serializers.CharField(max_length=255),
            "payment_details": inline_serializer(
                name="PaymentDetails",
                fields={
                    "payment_method": serializers.CharField(),
                    "amount": serializers.DecimalField(max_digits=10, decimal_places=2),
                    "currency": serializers.CharField(max_length=3, default="GHS"),
                    "phone_number": serializers.CharField(max_length=15),
                    "provider": serializers.CharField(max_length=20),
                },
            ),
        },
        required=["cart", "shipping_address"],
    ),
    responses={
        201: inline_serializer(
            name="CreateOrderResponse",
            fields={
                "detail": serializers.CharField(),
                "payment": PaymentSerializer(),
                "authorization_url": serializers.URLField(),
            },
        ),
    },
    tags=["Orders"],
)


sell_product_schema = extend_schema(
    summary="Sell a product offline",
    description="Sell products in-store",
    request=inline_serializer(
        name="SellProductRequest",
        fields={
            "products": serializers.ListField(
                child=inline_serializer(
                    name="ProductsRequestData",
                    fields={
                        "product": serializers.UUIDField(),
                        "quantity": serializers.IntegerField(min_value=1),
                    },
                )
            ),
        },
        required=["products"],
    ),
    responses={
        201: inline_serializer(
            name="SellProductResponse",
            fields={
                "detail": serializers.CharField(),
                "sale": OrderSerializer(),
            },
        ),
    },
    tags=["Orders"],
)


list_pending_orders_schema = extend_schema(
    summary="List Pending orders",
    description="List all pending orders",
    responses={
        200: OrderSerializer(many=True),
    },
    tags=["Orders"],
)

list_processing_orders_schema = extend_schema(
    summary="List orders in processing state",
    description="List all processing orders",
    responses={
        200: OrderSerializer(many=True),
    },
    tags=["Orders"],
)

update_order_status_schema = extend_schema(
    summary="Update order status",
    description="Update the status of an order",
    request=inline_serializer(
        name="UpdateOrderStatusRequest",
        fields={
            "status": serializers.ChoiceField(
                choices=["PENDING", "PROCESSING", "DELIVERED", "CANCELLED"]
            ),
        },
        required=["status"],
    ),
    responses={
        200: OrderSerializer(many=False),
    },
    tags=["Orders"],
)

delete_order_schema = extend_schema(
    summary="Delete an order",
    description="Delete an order",
    request=OrderSerializer,
    responses={
        204: inline_serializer(
            name="DeleteOrderResponse",
            fields={
                "detail": serializers.CharField(),
            },
        ),
    },
    tags=["Orders"],
)
