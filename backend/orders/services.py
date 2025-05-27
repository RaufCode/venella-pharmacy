from orders.models import Order, OrderItem
from orders.serializers import OrderSerializer, OrderItemSerializer
from orders.selectors import get_order_by_id
from products.models import Product
from products.selectors import get_product_by_id
from django.contrib.auth import get_user_model

User = get_user_model()
# IN_STORE_USER = User.objects.get(email="instoreuser@venella.com")


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


def sell_product(data: list):
    products = data.get("products", [])
    if not isinstance(products, list) or not products:
        return None, ["Products must be a non-empty list."]

    total_amount = 0
    for product_data in products:
        if not isinstance(product_data, dict):
            return None, ["Each product must be a dictionary."]
        if "id" not in product_data or "quantity" not in product_data:
            return None, ["Each product must have 'id' and 'quantity'."]

        product = get_product_by_id(product_data["id"])
        if not product:
            return None, ["Product not found."]

        if product.stock < product_data.get("quantity", 0):
            return None, ["Insufficient stock for the product."]

        product_data["amount"] = product.price
        total_amount += product_data["quantity"] * product.price

    order_serializer = OrderSerializer(
        data={
            "customer": IN_STORE_USER.id,
            "status": "DELIVERED",
            "order_type": "OFFLINE",
            "total_amount": total_amount,
            "shipping_address": "In-Store Purchase",
        }
    )

    if order_serializer.is_valid():
        order = order_serializer.save()

        for product_data in products:
            order_item_data = {
                "order": order.id,
                "product": product_data["id"],
                "quantity": product_data["quantity"],
                "amount": product_data["amount"],
            }
            order_item_serializer = OrderItemSerializer(data=order_item_data)
            if order_item_serializer.is_valid():
                order_item_serializer.save()
            else:
                return None, order_item_serializer.errors

        return order_serializer.data, None
    else:
        return None, order_serializer.errors
