from django.http import HttpRequest
from .models import Payment, PaymentMethod
from .serializers import PaymentSerializer, PaymentMethodSerializer


def payment_representation(
    payment: Payment, many: bool = False, request: HttpRequest = None
):
    return PaymentSerializer(payment, many=many, context={"request": request}).data


def payment_method_representation(
    payment_method: PaymentMethod, many: bool = False, request: HttpRequest = None
):
    return PaymentMethodSerializer(
        payment_method, many=many, context={"request": request}
    ).data


def get_payment_by_id(payment_id):
    try:
        payment = Payment.objects.get(id=payment_id)
    except Payment.DoesNotExist:
        return None
    else:
        return payment


def get_payments_by_order_id(order_id):
    payments = Payment.objects.filter(order__id=order_id)
    return payments


def get_payment_by_transaction_id(transaction_id):
    try:
        payment = Payment.objects.get(transaction_id=transaction_id)
    except Payment.DoesNotExist:
        return None
    else:
        return payment


def get_payments_by_customer_id(customer_id):
    payments = Payment.objects.filter(order__customer__id=customer_id)
    return payments


def get_payment_method_by_payment_id(payment_id):
    try:
        payment = Payment.objects.get(id=payment_id)
        return payment.payment_method
    except Payment.DoesNotExist:
        return None
    except PaymentMethod.DoesNotExist:
        return None
    else:
        return payment.payment_method
