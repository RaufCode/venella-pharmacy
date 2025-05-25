from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from products.selectors import *
from products.services import *
from core.utils.general import get_user_from_jwttoken
from documentations.products import *


class ProductViewSet(viewsets.ViewSet):

    # parser_classes = [
    #     "rest_framework.parsers.JSONParser",
    #     "rest_framework.parsers.MultiPartParser",
    # ]

    @list_products_schema
    def list_products(self, request):
        products = get_all_products()
        context = product_info(products, many=True)
        return Response(context, status=status.HTTP_200_OK)

    @retrieve_product_schema
    def retrieve_product(self, request, product_id):
        product = get_product_by_id(product_id)
        if not product:
            return Response(
                {"detail": "Product not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        context = product_info(product)
        return Response(context, status=status.HTTP_200_OK)

    @create_products_schema
    def add_product(self, request):
        user = get_user_from_jwttoken(request)
        if not user.role == "admin":
            return Response(
                {"error": "You do not have permission to add products."},
                status=status.HTTP_403_FORBIDDEN,
            )

        data = request.data
        product, errors = create_product(data)
        if not product:
            return Response(
                {"detail": "Could not add product", "errors": errors},
                status=status.HTTP_400_BAD_REQUEST,
            )
        context = product_info(product)
        return Response(context, status=status.HTTP_201_CREATED)

    @update_product_schema
    def update_product(self, request, product_id):
        user = get_user_from_jwttoken(request)
        if not user.role == "admin":
            return Response(
                {"error": "You do not have permission to update products."},
                status=status.HTTP_403_FORBIDDEN,
            )

        product = get_product_by_id(product_id)
        if not product:
            return Response(
                {"detail": "Product not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        data = request.data
        updated_product, errors = update_product(product, data)
        if not updated_product:
            return Response(
                {"detail": "Could not update product", "errors": errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        context = product_info(updated_product)
        return Response(context, status=status.HTTP_200_OK)

    @delete_product_schema
    def delete_product(self, request, product_id):
        user = get_user_from_jwttoken(request)
        if not user.role == "admin":
            return Response(
                {"error": "You do not have permission to delete products."},
                status=status.HTTP_403_FORBIDDEN,
            )

        product = get_product_by_id(product_id)
        if not product:
            return Response(
                {"detail": "Product not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        product.delete()
        return Response(
            {"detail": "Product deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )

    @search_products_schema
    def search_products(self, request):
        query = request.query_params.get("query", "")
        if not query:
            return Response(
                {"detail": "Query parameter is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        filtered_products = get_search_products(query)
        context = product_info(filtered_products, many=True)
        return Response(context, status=status.HTTP_200_OK)


class ProductCategoryViewSet(viewsets.ViewSet):
    @list_categories_schema
    def list_categories(self, request):
        categories = get_all_categories()
        context = category_info(categories, many=True)
        return Response(context, status=status.HTTP_200_OK)

    @retrieve_category_schema
    def retrieve_category(self, request, category_id):
        category = get_category_by_id(category_id)
        if not category:
            return Response(
                {"detail": "Category not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        context = category_info(category)
        return Response(context, status=status.HTTP_200_OK)

    @create_category_schema
    def create_category(self, request):
        data = request.data
        category, errors = create_product_category(data)
        if not category:
            return Response(
                {"detail": "Could not create category", "errors": errors},
                status=status.HTTP_400_BAD_REQUEST,
            )
        context = category_info(category)
        return Response(context, status=status.HTTP_201_CREATED)

    @update_category_schema
    def update_category(self, request, category_id):
        category = get_category_by_id(category_id)
        if not category:
            return Response(
                {"detail": "Category not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        data = request.data
        updated_category, errors = update_product_category(category, data)
        if not updated_category:
            return Response(
                {"detail": "Could not update category", "errors": errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        context = category_info(updated_category)
        return Response(context, status=status.HTTP_200_OK)

    @delete_category_schema
    def delete_category(self, request, category_id):
        category = get_category_by_id(category_id)
        if not category:
            return Response(
                {"detail": "Category not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        category.delete()
        return Response(
            {"detail": "Category deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )
