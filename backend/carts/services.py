from carts.models import Cart, CartItem
from carts.serializers import CartSerializer, CartItemSerializer


def create_cart_item(data: dict):
    """
    Create a new cart item with the provided data.
    """
    serializer = CartItemSerializer(data=data)
    if serializer.is_valid():
        cart_item = serializer.save()
        return cart_item, None
    return None, serializer.errors


def update_cart_item(cart_item: CartItem, data: dict):
    """
    Update an existing cart item with the provided data.
    """
    serializer = CartItemSerializer(cart_item, data=data, partial=True)
    if serializer.is_valid():
        updated_cart_item = serializer.save()
        return updated_cart_item, None
    return None, serializer.errors
