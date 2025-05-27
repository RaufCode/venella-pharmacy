from orders.models import Order, OrderItem
from orders.serializers import OrderSerializer, OrderItemSerializer
from orders.selectors import get_order_by_id
from products.models import Product
from products.selectors import get_product_by_id


def create_order(data: dict):
    serializer = OrderSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return serializer.data, None
    else:
        return None, serializer.errors


def create_order_items(data: dict):

    for order_item in data["order_items"]:
        product = get_product_by_id(order_item.get("product"))
        if not product:
            return None, [f"Product {order_item.get('product')} not found"]

        if product.stock < order_item.get("quantity", 0):
            return None, [f"Insufficient stock for product {product.name}"]

        if order_item.get("quantity") <= 0:
            return None, ["Quantity must be greater than zero"]

        if order_item.get("amount") <= 0:
            return None, ["Amount must be greater than zero"]

        order_item["order"] = data.get("order")

    serializer = OrderItemSerializer(data=data["order_items"], many=True)
    if serializer.is_valid():
        serializer.save()
        return serializer.data, None
    else:
        return None, serializer.errors
