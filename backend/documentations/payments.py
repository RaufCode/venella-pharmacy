from ._base import *
from payments.serializers import PaymentSerializer, PaymentMethodSerializer


initiate_payment_schema = extend_schema(
    summary="Initiate a payment for an order",
    description="Initiate a payment for a specific order using Paystack",
    request=inline_serializer(
        name="InitiatePaymentRequest",
        fields={
            "payment_method": serializers.CharField(),
            "amount": serializers.DecimalField(max_digits=10, decimal_places=2),
            "currency": serializers.CharField(max_length=3, default="GHS"),
            "phone_number": serializers.CharField(
                max_length=15, required=False, allow_blank=True
            ),
            "provider": serializers.CharField(
                max_length=20, required=False, allow_blank=True
            ),
        },
        required=["payment_method", "amount"],
    ),
    responses={
        200: PaymentSerializer(many=False),
    },
    tags=["Payments"],
)


verify_payment_schema = extend_schema(
    summary="Verify a payment",
    description="Verify a payment using Paystack",
    request=None,
    responses={
        200: PaymentSerializer(many=False),
    },
    tags=["Payments"],
)
