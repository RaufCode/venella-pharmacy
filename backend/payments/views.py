from rest_framework.response import Response
from rest_framework import status, viewsets
from .selectors import *
from .services import initiate_payment, verify_payment
from documentations.payments import initiate_payment_schema, verify_payment_schema


class PaymentViewSet(viewsets.ViewSet):

    @initiate_payment_schema
    def initialize_payment(self, request, order_id):
        """
        Initialize a payment for an order.
        """
        response, status_code = initiate_payment(order_id, request, request.data)

        return Response(response, status=status_code)

    @verify_payment_schema
    def verify_payment(self, request, payment_id):
        """
        Verify a payment by its ID.
        """
        response, status_code = verify_payment(payment_id, request)

        return Response(response, status=status_code)
