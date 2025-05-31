from django.urls import path
from .views import OrderViewSet

urlpatterns = [
    path("", OrderViewSet.as_view({"get": "list_orders"})),
    path("<str:order_id>/retrieve/", OrderViewSet.as_view({"get": "retrieve_order"})),
    path(
        "<str:order_id>/update-status/",
        OrderViewSet.as_view({"post": "update_order_status"}),
    ),
    path(
        "<str:order_id>/delete/",
        OrderViewSet.as_view({"delete": "delete_order"}),
    ),
    path("customer/orders/", OrderViewSet.as_view({"get": "list_customer_orders"})),
    path("create/", OrderViewSet.as_view({"post": "create_order"})),
    path("sell/", OrderViewSet.as_view({"post": "sell_in_store"})),
    path("pending/", OrderViewSet.as_view({"get": "list_pending_orders"})),
    path("processing/", OrderViewSet.as_view({"get": "list_processing_orders"})),
]
