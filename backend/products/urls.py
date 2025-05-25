from django.urls import path
from .views import ProductViewSet, ProductCategoryViewSet

urlpatterns = [
    path("", ProductViewSet.as_view({"get": "list_products"})),
    path(
        "<str:product_id>/retrieve/",
        ProductViewSet.as_view({"get": "retrieve_product"}),
    ),
    path("add/", ProductViewSet.as_view({"post": "add_product"})),
    path("<str:product_id>/update/", ProductViewSet.as_view({"put": "update_product"})),
    path(
        "<str:product_id>/delete/", ProductViewSet.as_view({"delete": "delete_product"})
    ),
    path(
        "search/",
        ProductViewSet.as_view({"get": "search_products"}),
    ),
    # Product Categories
    path("categories/", ProductCategoryViewSet.as_view({"get": "list_categories"})),
    path(
        "categories/<str:category_id>/retrieve/",
        ProductCategoryViewSet.as_view({"get": "retrieve_category"}),
    ),
    path(
        "categories/add/",
        ProductCategoryViewSet.as_view({"post": "create_category"}),
    ),
    path(
        "categories/<str:category_id>/update/",
        ProductCategoryViewSet.as_view({"put": "update_category"}),
    ),
    path(
        "categories/<str:category_id>/delete/",
        ProductCategoryViewSet.as_view({"delete": "delete_category"}),
    ),
]
