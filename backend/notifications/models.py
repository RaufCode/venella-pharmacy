import uuid
from django.db import models
from core.models.accounts import UserAccount


class Notification(models.Model):
    NOTIFICATION_TYPE_CHOICES = (
        ('NEW_ORDER', 'New Order'),
        ('ORDER_STATUS_UPDATE', 'Order Status Update'),
        ('PRODUCT_STOCK_ALERT', 'Product Stock Alert'),
        ('NEW_MESSAGE', 'New Message'),
        ('SYSTEM_ALERT', 'System Alert'),
        ('PROMOTION', 'Promotion'),
        ('OTHER', 'Other'),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type = models.CharField(max_length=50, choices=NOTIFICATION_TYPE_CHOICES)
    content = models.TextField(blank=True, null=True)
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_type_display()} - {'Read' if self.read else 'Unread'}"
    
    def get_type_display(self):
        return dict(self.NOTIFICATION_TYPE_CHOICES).get(self.type, 'Unknown Type')
    

class CustomerNotification(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE, related_name='notifications')
    customer = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name='customer_notifications')

    def __str__(self):
        return f"Notification for {self.user.profile.first_name}: {self.notification.get_type_display()} - {'Read' if self.notification.read else 'Unread'}"