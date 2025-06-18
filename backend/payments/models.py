from uuid import uuid4
from django.db import models
from orders.models import Order


class PaymentMethod(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    method_type = models.CharField(
        max_length=20,
        choices=[
            ("card", "Card"),
            ("bank_transfer", "Bank Transfer"),
            ("mobile_money", "Mobile Money"),
        ],
    )
    details = models.JSONField()

    def __str__(self):
        return f"{self.method_type}"


class Payment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="payments")
    payment_method = models.ForeignKey(
        PaymentMethod,
        on_delete=models.CASCADE,
        related_name="payments",
        null=True,
        blank=True,
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default="GHS")
    status = models.CharField(
        max_length=20,
        choices=[
            ("pending", "Pending"),
            ("completed", "Completed"),
            ("failed", "Failed"),
            ("refunded", "Refunded"),
        ],
        default="pending",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    transaction_id = models.CharField(
        max_length=100, unique=True, null=True, blank=True
    )

    def __str__(self):
        return f"Payment {self.id} for Order {self.order.id}"
