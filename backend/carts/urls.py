from django.urls import path
from carts.views import CartItemViewSet


urlpatterns = [
    path("", CartItemViewSet.as_view({"get": "list"})),
    path("cart-items/", CartItemViewSet.as_view({"get": "list_cart_items"})),
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
