from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import (
    ServiceProviderServicesTransactionSerializer,
    ServiceProviderProductsTransactionSerializer
)
from .models import (
    ServiceProviderServicesTransaction,
    ServiceProviderProductsTransaction
)
from appointment_booking.models import AppointmentCheckout
from accounts.models import CustomUser
from services.models import Service
from professional_service_provider.models import ServiceProviderProfile
from products.models import Product, ProductOrder
import braintree
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from decouple import config
from rest_framework.permissions import IsAuthenticated


class BrainTreeTokenGenerationView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Generate token for braintree payment gateway.",
        responses={
            200: openapi.Response(
                description="Token generated successfully.",
                examples={
                    "application/json": {
                        "token": "sandbox_9z7q3g6x_8n4q9y3v8qy3zq4n"
                    }
                }
            )
        }
    )
    def get(self, request, *args, **kwargs):
        # setting environeent variable for braintree to be sandbox during development
        gateway = braintree.BraintreeGateway(
            braintree.Configuration(
                braintree.Environment.Sandbox,
                merchant_id=config('BRAINTREE_MERCHANT_ID'),
                public_key=config('BRAINTREE_PUBLIC_KEY'),
                private_key=config('BRAINTREE_PRIVATE_KEY')
            )
        )
        user = request.user
        try:
            braintree_client_token = gateway.client_token.generate(
                {"customer_id": str(user.id)}
            )
        except ValueError:
            braintree_client_token = gateway.client_token.generate()

        response = {
            "status": "success",
            "message": "Token generated successfully.",
            "token": braintree_client_token
        }
        return Response(response, status=status.HTTP_200_OK)


class BrainTreePaymentProcessingView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Process payment using braintree payment gateway.",
        responses={
            200: openapi.Response(
                description="Payment processed successfully.",
                examples={
                    "application/json": {
                        "status": "success",
                        "message": "Payment processed successfully.",
                        "transaction": {
                            "id": "6w2n8z",
                            "type": "sale",
                            "amount": "10.00",
                            "status": "authorized",
                            "created_at": "2021-04-12T13:06:48Z",
                            "updated_at": "2021-04-12T13:06:48Z",
                        }
                    }
                }
            )
        }
    )
    def post(self, request, *args, **kwargs):
        # setting environeent variable for braintree to be sandbox during development
        gateway = braintree.BraintreeGateway(
            braintree.Configuration(
                braintree.Environment.Sandbox,
                merchant_id=config('BRAINTREE_MERCHANT_ID'),
                public_key=config('BRAINTREE_PUBLIC_KEY'),
                private_key=config('BRAINTREE_PRIVATE_KEY')
            )
        )
        user = request.user
        # create a new customer in braintree
        new_user = gateway.customer.create({
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
        })

        # create a new payment method for the customer
        nonce_from_the_client = request.data.get("payment_method_nonce")
        amount = request.data.get("amount")
        result = gateway.transaction.sale({
            "customer_id": new_user.customer.id,
            "amount": amount,
            "payment_method_nonce": nonce_from_the_client,
            "options": {
                "submit_for_settlement": True
            }
        })
        if result.is_success:
            # save transaction details to database
            current_url = request.build_absolute_uri()
            #if 'appointment' in current_url:

            response = {
                "status": "success",
                "message": "Payment processed successfully.",
                "transaction": result.transaction
            }
            return Response(response, status=status.HTTP_200_OK)
        else:
            response = {
                "status": "failed",
                "message": "Payment processing failed.",
                "error": result.message
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

