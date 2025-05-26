from orders.serializers import OrderSerializer
from orders.models import Order


def get_all_orders():
    return Order.objects.all()


def get_order_by_id(order_id: str):
    try:
        return Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return None


def get_orders_by_customer(customer_id: str):
    return Order.objects.filter(customer=customer_id)


def get_customer_orders_by_status(customer: str, status: str):
    return Order.objects.filter(customer=customer, status=status)


def order_representation(order: Order, many: bool = False):
    serializer = OrderSerializer(order, many=many)
    return serializer.data
