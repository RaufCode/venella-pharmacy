import json
import requests
from django.conf import settings
from rest_framework import status
from .models import Payment, PaymentMethod
from .serializers import PaymentSerializer, PaymentMethodSerializer
from .selectors import *
from orders.selectors import get_order_by_id
from orders.models import Order


def initiate_payment(order_id, request):
    """
    Initialize a payment for an order.
    """
    data = request.data
    if not data:
        return {"error": "No data provided"}, status.HTTP_400_BAD_REQUEST

    try:
        order = get_order_by_id(order_id)
    except Order.DoesNotExist:
        return {"error": "Order not found"}, status.HTTP_404_NOT_FOUND

    if not data.get("payment_method"):
        return {"error": "Payment method is required"}, status.HTTP_400_BAD_REQUEST

    payment_method_data = {
        "method_type": data.get("payment_method"),
        "details": json.dumps(
            {
                "phone_number": data.get("phone_number", ""),
                "provider": data.get("provider", ""),
            }
        ),
    }
    payment_method_serializer = PaymentMethodSerializer(data=payment_method_data)
    if not payment_method_serializer.is_valid():
        return {"error": payment_method_serializer.errors}, status.HTTP_400_BAD_REQUEST

    payment_method = payment_method_serializer.save()

    payment_data = {
        "order": order.id,
        "payment_method": payment_method.id,
        "amount": data.get("amount", order.total_amount),
        "currency": data.get("currency", "GHS"),
    }

    payment_serializer = PaymentSerializer(data=payment_data)
    if not payment_serializer.is_valid():
        return {"error": payment_serializer.errors}, status.HTTP_400_BAD_REQUEST

    payment = payment_serializer.save()

    # paystack integration
    paystack_data = {
        "amount": int(payment.amount * 100),  # Paystack expects amount in kobo
        "currency": payment.currency,
        "email": order.customer.email,
        "ref": str(payment.id),
        "callback_url": f"{request.build_absolute_uri('/payments/callback/')}",
        "metadata": {
            "payment_id": str(payment.id),
            "order_id": str(order.id),
        },
    }

    if data.get("payment_method") == "mobile_money":
        paystack_data["mobile_money"] = {
            "phone_number": data.get("phone_number"),
            "provider": data.get("providder"),
        }

    headers = {
        "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
        "Content-Type": "application/json",
    }

    try:
        response = requests.post(
            "https://api.paystack.co/transaction/initialize",
            headers=headers,
            data=json.dumps(paystack_data),
        )
        response_data = response.json()
        if response.status_code != 200:
            return {
                "error": response_data.get("message", "Payment initialization failed")
            }, status.HTTP_400_BAD_REQUEST
        payment.transaction_id = response_data["data"]["reference"]
        payment.status = "pending"
        payment.save()
        return {
            "message": "Payment initialized successfully",
            "payment": payment_representation(payment, many=False, request=request),
            "authorization_url": response_data["data"]["authorization_url"],
        }, status.HTTP_200_OK

    except requests.RequestException as e:
        return {"error": str(e)}, status.HTTP_500_INTERNAL_SERVER_ERROR


def verify_payment(payment_id, request):
    """
    Verify a payment using Paystack.
    """
    try:
        payment = get_payment_by_id(payment_id)
    except Payment.DoesNotExist:
        return {"error": "Payment not found"}, status.HTTP_404_NOT_FOUND

    headers = {
        "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
        "Content-Type": "application/json",
    }

    try:
        response = requests.get(
            f"https://api.paystack.co/transaction/verify/{payment.transaction_id}",
            headers=headers,
        )
        response_data = response.json()
        if response.status_code != 200:
            return {
                "error": response_data.get("message", "Payment verification failed")
            }, status.HTTP_400_BAD_REQUEST

        # Update payment status based on Paystack response
        if response_data["data"]["status"] == "success":
            payment.status = "completed"
        else:
            payment.status = "failed"

        payment.save()
        return {
            "message": "Payment verified successfully",
            "payment": payment_representation(payment, many=False, request=request),
        }, status.HTTP_200_OK

    except requests.RequestException as e:
        return {"error": str(e)}, status.HTTP_500_INTERNAL_SERVER_ERROR
