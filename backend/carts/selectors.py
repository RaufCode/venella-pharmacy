from django.http import HttpRequest
from carts.serializers import CartSerializer, CartItemSerializer
from carts.models import Cart, CartItem


def get_all_carts():
    """
    Retrieve all carts from the database.
    """
    return Cart.objects.all()


def get_cart_by_customer(customer_id: str):
    """
    Retrieve the cart for a specific customer.
    If no cart exists, create a new one.
    """
    cart, created = Cart.objects.get_or_create(customer_id=customer_id)
    return cart, created


def get_cart_by_id(cart_id: str):
    try:
        return Cart.objects.get(id=cart_id)
    except Cart.DoesNotExist:
        return None


def get_all_cart_items():
    return CartItem.objects.all()


def get_cart_items(cart_id: str):
    return CartItem.objects.filter(cart_id=cart_id)


def get_cart_item_by_id(cart_item_id: str):

    try:
        return CartItem.objects.get(id=cart_item_id)
    except CartItem.DoesNotExist:
        return None


def cart_representation(request: HttpRequest, cart: Cart, many: bool = False):
    serializer = CartSerializer(cart, many=many, context={"request": request})
    return serializer.data


def cart_item_representation(
    request: HttpRequest, cart_item: CartItem, many: bool = False
):
    serializer = CartItemSerializer(cart_item, many=many, context={"request": request})
    return serializer.data
