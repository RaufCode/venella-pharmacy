from django.http import HttpRequest
from orders.serializers import OrderSerializer
from orders.models import Order


def get_all_orders():
    return Order.objects.all()


def get_order_by_id(order_id: str):
    try:
        return Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return None


def get_orders_by_status(status: str):
    return Order.objects.filter(status=status).order_by("status")


def get_orders_by_statuses(statuses: list):
    return Order.objects.filter(status__in=statuses).order_by("status")


def get_orders_by_customer(customer_id: str):
    return Order.objects.filter(customer=customer_id).order_by("status")


def get_customer_orders_by_status(customer: str, status: str):
    return Order.objects.filter(customer=customer, status=status).order_by("status")


def order_representation(request: HttpRequest, order: Order, many: bool = False):
    serializer = OrderSerializer(order, many=many, context={"request": request})
    return serializer.data
