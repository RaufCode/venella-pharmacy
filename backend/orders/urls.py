from django.urls import path
from .views import OrderViewSet

urlpatterns = [
    path("", OrderViewSet.as_view({"get": "list_orders"})),
    path("<str:order_id>/retrieve/", OrderViewSet.as_view({"get": "retrieve_order"})),
    path("customer/orders/", OrderViewSet.as_view({"get": "list_customer_orders"})),
    path("create/", OrderViewSet.as_view({"post": "create_order"})),
]
