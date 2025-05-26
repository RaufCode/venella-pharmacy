from orders.models import Order, OrderItems
from orders.serializers import OrderSerializer, OrderItemsSerializer
from orders.selectors import get_order_by_id
from products.models import Product
from products.selectors import get_product_by_id
from core.models.accounts import UserAccount
from core.utils.general import validate_posted_data


def create_order(data: dict):
    err, errors = validate_posted_data(
        data, ["customer", "total_amount", "shipping_address", "order_items"]
    )
    if err:
        return None, errors

    if not isinstance(data.get("order_items"), list) or not data["order_items"]:
        return None, ["Order items must be a non-empty list"]

    err, errors = validate_posted_data(
        data["order_items"], ["product", "quantity", "amount"]
    )
    if err:
        return None, errors

    serializer = OrderSerializer(data=data)
    if serializer.is_valid():
        order = serializer.save()
        return order.data
    else:
        return None, serializer.errors


def create_order_items(data: dict):

    for order_item in data["order_items"]:
        product = get_product_by_id(order_item.get("product"))
        if not product:
            return None, [f"Product {order_item.get('product')} not found"]

        if order_item.get("quantity") <= 0:
            return None, ["Quantity must be greater than zero"]

        if order_item.get("amount") <= 0:
            return None, ["Amount must be greater than zero"]

        order_item["order"] = data.get("order")

    serializer = OrderItemsSerializer(data=data["order_items"], many=True)
    if serializer.is_valid():
        serializer.save()
        return serializer.data, None
    else:
        return None, serializer.errors
