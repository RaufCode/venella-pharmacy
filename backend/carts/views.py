from rest_framework import viewsets, status
from rest_framework.response import Response
from carts.selectors import *
from carts.services import *
from core.utils.general import get_user_from_jwttoken, validate_posted_data
from documentations.carts import *


class CartItemViewSet(viewsets.ViewSet):

    @list_all_cart_items_schema
    def list(self, request):
        cart_items = get_all_cart_items()
        context = cart_item_representation(cart_items, many=True)
        return Response(context, status=status.HTTP_200_OK)

    @list_customer_cart_items_schema
    def list_cart_items(self, request):
        user = get_user_from_jwttoken(request)
        if not user:
            return Response(
                {"detail": "Authentication credentials were not provided."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        cart, created = get_cart_by_customer(user.id)
        if not cart:
            return Response(
                {"detail": "Cart not found."}, status=status.HTTP_404_NOT_FOUND
            )

        cart_items = get_cart_items(cart.id)
        context = cart_item_representation(cart_items, many=True)
        return Response(context, status=status.HTTP_200_OK)

    @add_cart_item_schema
    def add_item_to_cart(self, request):
        user = get_user_from_jwttoken(request)
        if not user:
            return Response(
                {"detail": "Authentication credentials were not provided."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        cart, created = get_cart_by_customer(user.id)
        if not cart:
            return Response(
                {"detail": "Cart not found."}, status=status.HTTP_404_NOT_FOUND
            )
        data = request.data
        err, errors = validate_posted_data(data, ["product", "quantity"])
        if err:
            return Response(
                {"detail": "Invalid data.", "errors": errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        data["cart"] = cart.id
        cart_item, errors = create_cart_item(data)
        if not cart_item:
            return Response(
                {"detail": "Failed to create cart item.", "errors": errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        context = {
            "detail": "Cart item created successfully.",
            "item": cart_item_representation(cart_item),
        }
        return Response(context, status=status.HTTP_201_CREATED)

    @update_cart_item_schema
    def update_cart_item(self, request, item_id):
        user = get_user_from_jwttoken(request)
        if not user:
            return Response(
                {"detail": "Authentication credentials were not provided."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        cart_item = get_cart_item_by_id(item_id)
        if not cart_item:
            return Response(
                {"detail": "Cart item not found."}, status=status.HTTP_404_NOT_FOUND
            )
        data = request.data

        updated_cart_item, errors = update_cart_item(cart_item, data)
        if not updated_cart_item:
            return Response(
                {"detail": "Failed to update cart item.", "errors": errors},
                status=status.HTTP_400_BAD_REQUEST,
            )
        context = {
            "detail": "Cart item updated successfully.",
            "item": cart_item_representation(updated_cart_item),
        }
        return Response(context, status=status.HTTP_200_OK)

    @delete_cart_item_schema
    def remove_item_from_cart(self, request, item_id):
        user = get_user_from_jwttoken(request)
        if not user:
            return Response(
                {"detail": "Authentication credentials were not provided."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        cart_item = get_cart_item_by_id(item_id)
        if not cart_item:
            return Response(
                {"detail": "Cart item not found."}, status=status.HTTP_404_NOT_FOUND
            )

        cart_item.delete()
        return Response(
            {"detail": "Cart item removed successfully."},
            status=status.HTTP_204_NO_CONTENT,
        )
