from rest_framework import viewsets, status
from rest_framework.response import Response
from core.utils.general import get_user_from_jwttoken, validate_posted_data
from orders.selectors import *
from orders.services import *
from carts.selectors import *
from carts.services import clear_cart
from notifications.services import (
    create_customer_notification,
    create_salesperson_notification,
)
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

        orders = [
            order for order in get_orders_by_customer(user.id) if not order.deleted
        ]
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

        # Update product stock
        for item in order_items:
            product = get_product_by_id(item["product"])
            if product:
                product.stock -= item["quantity"]
                product.save()

                # Check for low stock after reducing inventory
                from products.services import check_and_send_low_stock_notification

                check_and_send_low_stock_notification(product)

        # Clear the cart after order creation
        clear_cart(cart.id)

        create_customer_notification(
            {
                "customer": user.id,
                "type": "NEW_ORDER",
                "content": f"Your order #{order.id} has been placed successfully and waiting to be processed. Thank you for shopping with us!",
            }
        )
        create_salesperson_notification(
            {
                "type": "NEW_ORDER",
                "content": f"A new order #{order.id} has been placed by {user.email}.",
            }
        )

        context = order_representation(request, order, many=False)
        return Response(context, status=status.HTTP_201_CREATED)

    @sell_product_schema
    def sell_in_store(self, request):
        user = get_user_from_jwttoken(request)
        if not user:
            return Response(
                {"detail": "Authentication credentials were not provided."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        data = request.data
        err, errors = validate_posted_data(data, ["products"])
        if err:
            return Response({"detail": errors}, status=status.HTTP_400_BAD_REQUEST)

        sale, errors = sell_product(data)
        if not sale:
            return Response({"detail": errors}, status=status.HTTP_400_BAD_REQUEST)

        order = get_order_by_id(sale["id"])

        # Update product stock
        for item in data.get("products"):
            product = get_product_by_id(item["product"])
            if product:
                product.stock -= item["quantity"]
                product.save()

                # Check for low stock after reducing inventory
                from products.services import check_and_send_low_stock_notification

                check_and_send_low_stock_notification(product)

        context = {
            "detail": "Sale processed successfully.",
            "sale": order_representation(request, order),
        }
        return Response(context, status=status.HTTP_200_OK)

    @list_pending_orders_schema
    def list_pending_orders(self, request):
        """List orders placed by customers to the store 'Pending and Processing'."""
        orders = get_orders_by_status("PENDING")
        context = order_representation(request, orders, many=True)
        return Response(context, status=status.HTTP_200_OK)

    @list_processing_orders_schema
    def list_processing_orders(self, request):
        orders = get_orders_by_status("PROCESSING")
        context = order_representation(request, orders, many=True)
        return Response(context, status=status.HTTP_200_OK)

    @update_order_status_schema
    def update_order_status(self, request, order_id):
        """Update the status of an order."""
        user = get_user_from_jwttoken(request)
        if not user:
            return Response(
                {"detail": "Authentication credentials were not provided."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        order = get_order_by_id(order_id)
        if not order:
            return Response(
                {"detail": "Order not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        data = request.data
        new_status = data.get("status").strip().upper()
        if new_status not in dict(order.ORDER_STATUS_CHOICES).keys():
            return Response(
                {"detail": "Invalid status provided."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        order.status = new_status
        order.save()

        if new_status == "PROCESSING":
            create_salesperson_notification(
                {
                    "type": "ORDER_STATUS_UPDATE",
                    "content": f"Order #{order.id} is now being processed.",
                }
            )
            create_customer_notification(
                {
                    "customer": order.customer.id,
                    "type": "ORDER_STATUS_UPDATE",
                    "content": f"Your order #{order.id} is now being processed.",
                }
            )
        elif new_status == "DELIVERED":
            create_salesperson_notification(
                {
                    "type": "ORDER_STATUS_UPDATE",
                    "content": f"Order #{order.id} has been delivered.",
                }
            )
            create_customer_notification(
                {
                    "customer": order.customer.id,
                    "type": "ORDER_STATUS_UPDATE",
                    "content": f"Your order #{order.id} has been delivered. Thank you for shopping with us!",
                }
            )
        elif new_status == "CANCELLED":
            create_salesperson_notification(
                {
                    "type": "ORDER_STATUS_UPDATE",
                    "content": f"Order #{order.id} has been cancelled.",
                }
            )
            create_customer_notification(
                {
                    "customer": order.customer.id,
                    "type": "ORDER_STATUS_UPDATE",
                    "content": f"Your order #{order.id} has been cancelled. We apologize for the inconvenience.",
                }
            )

        context = order_representation(request, order)
        return Response(context, status=status.HTTP_200_OK)

    @delete_order_schema
    def delete_order(self, request, order_id):
        """Delete an order."""
        user = get_user_from_jwttoken(request)
        if not user:
            return Response(
                {"detail": "Authentication credentials were not provided."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        order = get_order_by_id(order_id)
        if not order:
            return Response(
                {"detail": "Order not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        if order.deleted:
            return Response(
                {"detail": "Order has already been deleted."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        deleted_order, error = delete_order(order)
        if not deleted_order:
            return Response(
                {"detail": "Failed to delete order.", "error": error},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {"detail": "Order deleted successfully."}, status=status.HTTP_204_NO_CONTENT
        )
