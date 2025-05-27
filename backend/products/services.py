from products.models import Product, ProductCategory, ProductImage
from products.serializers import (
    ProductSerializer,
    ProductCategorySerializer,
    ProductImageSerializer,
)
from products.selectors import get_product_by_id
from core.utils.general import InMemoryUploadedFileHandler


def create_product(data: dict):
    product_images = data.pop("product_images", None)
    if not product_images:
        return None, ["Product images is not included"]

    if not isinstance(product_images, list):
        return None, ["Product images should be a list"]
    else:
        fhandler = InMemoryUploadedFileHandler()
        print("Product images:", product_images)
        product_images = [
            image if not isinstance(image, str) else fhandler.from_img_path(image)
            for image in product_images
        ]

    product_data = {
        "name": data.get("name"),
        "description": data.get("description"),
        "price": data.get("price"),
        "stock": data.get("stock"),
        "category": data.get("category"),
    }
    serializer = ProductSerializer(data=product_data)
    if serializer.is_valid():
        serializer.save()
    else:
        return None, serializer.errors

    product = get_product_by_id(serializer.data.get("id"))
    if not product:
        return None, ["Product could not be created"]
    print("product images:", product_images)
    image_data = []
    for image in product_images:
        image_data.append({"image": image, "product": product.id})
    print("Image data:", image_data)
    image_serializer = ProductImageSerializer(data=image_data, many=True)
    if image_serializer.is_valid():
        image_serializer.save()
    else:
        product.delete()
        return None, image_serializer.errors

    return product, None


def update_product(product: Product, data: dict):
    product_serializer = ProductSerializer(product, data=data, partial=True)
    if product_serializer.is_valid():
        product_serializer.save()
    else:
        return None, product_serializer.errors

    product = get_product_by_id(product_serializer.data.get("id"))

    product_images = data.get("product_images")
    if product_images:
        if not isinstance(product_images, list):
            return None, ["Product images should be a list"]
        fhandler = InMemoryUploadedFileHandler()
        product_images = [
            {"image": fhandler.from_img_path(image_data.get("image"))}
            for image_data in product_images
            if isinstance(image_data.get("image"), str)
        ]
        product_images = [
            image_data.update({"product": product.id}) for image_data in product_images
        ]
        image_serializer = ProductImageSerializer(data=product_images, many=True)
        if image_serializer.is_valid():
            image_serializer.save()
        else:
            return None, image_serializer.errors

    return product, None


def create_product_category(data: dict):
    serializer = ProductCategorySerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return serializer.data, None
    else:
        return None, serializer.errors


def update_product_category(category: ProductCategory, data: dict):
    serializer = ProductCategorySerializer(category, data=data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return serializer.data, None
    else:
        return None, serializer.errors
