from products.models import Product, ProductCategory
from products.serializers import ProductSerializer, ProductCategorySerializer


def get_all_products():
    products = Product.objects.all()
    return products


def get_product_by_id(product_id: str):
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return None
    else:
        return product


def get_search_products(query: str):
    products = Product.objects.filter(name__icontains=query)
    return products


def product_info(product: Product, many: bool = False):
    serializer = ProductSerializer(product, many=many)
    return serializer.data


def get_all_categories():
    categories = ProductCategory.objects.all()
    return categories


def get_category_by_id(category_id: str):
    try:
        category = ProductCategory.objects.get(id=category_id)
    except ProductCategory.DoesNotExist:
        return None
    else:
        return category


def category_info(category: ProductCategory, many: bool = False):
    serializer = ProductCategorySerializer(category, many=many)
    return serializer.data
