from django.contrib import admin
from notifications.models import (
    Notification,
    CustomerNotification,
    SalesPersonNotification,
)

# Register your models here.
admin.site.register(Notification)
admin.site.register(CustomerNotification)
admin.site.register(SalesPersonNotification)
