import uuid
from django.db import models
from core.models.accounts import UserAccount
from products.models import Product


class Order(models.Model):
    ORDER_STATUS_CHOICES = (
        ("PENDING", "Pending"),
        ("PROCESSING", "Processing"),
        ("DELIVERED", "Delivered"),
        ("CANCELLED", "Cancelled"),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(
        UserAccount, related_name="orders", on_delete=models.CASCADE
    )
    sales_person = models.ForeignKey(
        UserAccount,
        null=True,
        related_name="processed_orders",
        on_delete=models.SET_NULL,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20, choices=ORDER_STATUS_CHOICES, default="PENDING"
    )
    order_type = models.CharField(
        max_length=20,
        choices=[("ONLINE", "Online"), ("OFFLINE", "Offline")],
        default="ONLINE",
    )
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_address = models.TextField()

    def __str__(self):
        return f"Order by {self.customer} - {self.status}"

    def order_items(self):
        return self.items.all()

    @property
    def deleted(self):
        return hasattr(self, "deletedorder")

    @property
    def payment_status(self):
        if hasattr(self, "payments"):
            payments = self.payments.all().order_by("-created_at")
            if payments.exists():
                return payments.first().status
            # return "UNPAID"
        return "UNPAID"

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Order"
        verbose_name_plural = "Orders"


class OrderItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, related_name="order_items", on_delete=models.CASCADE
    )
    quantity = models.IntegerField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} for {self.order.customer}"


class DeletedOrder(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.OneToOneField(
        Order, related_name="deleted_order", on_delete=models.CASCADE
    )
    deleted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Deleted Order {self.order.id} at {self.deleted_at}"
