from rest_framework import viewsets, status
from rest_framework.response import Response
from orders.selectors import *
from orders.services import *
from core.utils.general import get_user_from_jwttoken


class OrderViewSet(viewsets.ViewSet):
    def list_orders(self, request):
        orders = get_all_orders()
        context = order_representation(orders, many=True)
        return Response(context, status=status.HTTP_200_OK)

    def retrieve_order(self, request, order_id):
        order = get_order_by_id(order_id)
        if not order:
            context = {"detail": "Order not found."}
            return Response(context, status=status.HTTP_404_NOT_FOUND)

        context = order_representation(order, many=False)
        return Response(context, status=status.HTTP_200_OK)

    def list_customer_orders(self, request):
        user = get_user_from_jwttoken(request)
        if not user:
            context = {"detail": "Authentication credentials were not provided."}
            return Response(context, status=status.HTTP_401_UNAUTHORIZED)

        orders = get_orders_by_customer(user.id)
        context = order_representation(orders, many=True)
        return Response(context, status=status.HTTP_200_OK)

    def create_order(self, request):
        user = get_user_from_jwttoken(request)
        if not user:
            context = {"detail": "Authentication credentials were not provided."}
            return Response(context, status=status.HTTP_401_UNAUTHORIZED)

        data = request.data
        data["customer"] = user.id

        order_data, errors = create_order(data)
        if not order_data:
            context = {"detail": errors}
            return Response(context, status=status.HTTP_400_BAD_REQUEST)

        order = get_order_by_id(order_data["id"])
        if not order:
            context = {"detail": "Order creation failed."}
            return Response(context, status=status.HTTP_400_BAD_REQUEST)

        order_items = {"order": order.id, "order_items": data.get("order_items")}
        order_items_data, errors = create_order_items(order_items)
        if not order_items_data:
            context = {"detail": errors}
            return Response(context, status=status.HTTP_400_BAD_REQUEST)

        context = order_representation(order, many=False)
        return Response(context, status=status.HTTP_201_CREATED)
