from django.urls import path
from carts.views import CartItemViewSet, CartViewSet


urlpatterns = [
    path("", CartViewSet.as_view({"get": "list"})),
    path("<str:cart_id>/retrieve/", CartViewSet.as_view({"get": "retrieve_cart"})),
    path("cart-items/", CartItemViewSet.as_view({"get": "list"})),
    path(
        "cart-items/<str:item_id>/retrieve/",
        CartItemViewSet.as_view({"get": "retrieve"}),
    ),
    path(
        "customer/cart-items/",
        CartItemViewSet.as_view({"get": "list_customer_cart_items"}),
    ),
    path("cart-items/add/", CartItemViewSet.as_view({"post": "add_item_to_cart"})),
    path(
        "cart-item/<str:item_id>/update/",
        CartItemViewSet.as_view({"put": "update_cart_item"}),
    ),
    path(
        "cart-item/<str:item_id>/delete/",
        CartItemViewSet.as_view({"delete": "remove_item_from_cart"}),
    ),
]
