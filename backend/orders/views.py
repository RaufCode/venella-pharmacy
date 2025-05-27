from rest_framework import viewsets, status
from rest_framework.response import Response
from orders.selectors import *
from orders.services import *
from carts.selectors import *
from core.utils.general import get_user_from_jwttoken, validate_posted_data
from documentations.orders import *


class OrderViewSet(viewsets.ViewSet):
    @list_orders_schema
    def list_orders(self, request):
        orders = get_all_orders()
        context = order_representation(request, orders, many=True)
        return Response(context, status=status.HTTP_200_OK)

    @retrieve_order_schema
    def retrieve_order(self, request, order_id):
        order = get_order_by_id(order_id)
        if not order:
            context = {"detail": "Order not found."}
            return Response(context, status=status.HTTP_404_NOT_FOUND)

        context = order_representation(request, order, many=False)
        return Response(context, status=status.HTTP_200_OK)

    @list_customer_orders_schema
    def list_customer_orders(self, request):
        user = get_user_from_jwttoken(request)
        if not user:
            context = {"detail": "Authentication credentials were not provided."}
            return Response(context, status=status.HTTP_401_UNAUTHORIZED)

        orders = get_orders_by_customer(user.id)
        context = order_representation(request, orders, many=True)
        return Response(context, status=status.HTTP_200_OK)

    @create_order_schema
    def create_order(self, request):
        user = get_user_from_jwttoken(request)
        if not user:
            return Response(
                {"detail": "Authentication credentials were not provided."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        data = request.data
        err, errors = validate_posted_data(data, ["cart", "shipping_address"])
        if err:
            return Response({"detail": errors}, status=status.HTTP_400_BAD_REQUEST)

        data["customer"] = user.id

        cart = get_cart_by_id(data.get("cart"))
        if not cart:
            return Response(
                {"detail": "Cart not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        if cart.customer != user:
            return Response(
                {"detail": "Cart does not belong to the authenticated user."},
                status=status.HTTP_403_FORBIDDEN,
            )

        cart_items = get_cart_items(cart.id)
        if not cart_items:
            return Response(
                {"detail": "Cart is empty."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        print("Cart items:", cart_items)
        order_items = [
            {
                "product": item.product.id,
                "quantity": item.quantity,
                "amount": item.product.price,
            }
            for item in cart_items
        ]
        data["order_items"] = order_items
        data["total_amount"] = sum(
            item["quantity"] * item["amount"] for item in order_items
        )
        print("order data:", data)
        order_data, errors = create_order(data)
        if not order_data:
            return Response(
                {"detail": errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        order = get_order_by_id(order_data["id"])
        if not order:
            return Response(
                {"detail": "Order creation failed."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        order_items_payload = {"order": order.id, "order_items": order_items}
        order_items_data, errors = create_order_items(order_items_payload)
        if not order_items_data:
            return Response(
                {"detail": errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        context = order_representation(request, order, many=False)
        return Response(context, status=status.HTTP_201_CREATED)
