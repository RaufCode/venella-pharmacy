import uuid
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class ProductCategory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    # description = models.TextField()

    def __str__(self):
        return self.name


class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    brand = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    category = models.ForeignKey(
        ProductCategory, related_name="products", on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(
        Product, related_name="images", on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to="venella/products/images/")

    def __str__(self):
        return f"Image for {self.product.name}"


@receiver(post_save, sender=Product)
def check_low_stock(sender, instance, created, **kwargs):
    """
    Signal handler to check for low stock and send notifications
    when product stock is 10 or less
    """
    if instance.stock <= 10:
        from notifications.services import create_salesperson_notification

        # Send notification to all salespersons about low stock
        create_salesperson_notification(
            {
                "type": "PRODUCT_STOCK_ALERT",
                "content": f"Low Stock Alert: {instance.name} has only {instance.stock} units remaining. Please restock soon.",
            }
        )
