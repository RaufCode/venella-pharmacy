from django.urls import path
from .views import PaymentViewSet

urlpatterns = [
    path(
        "initiate/<str:order_id>/",
        PaymentViewSet.as_view({"post": "initialize_payment"}),
    ),
    path("verify/<str:reference>/", PaymentViewSet.as_view({"post": "verify_payment"})),
]
