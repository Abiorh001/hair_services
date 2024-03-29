from django.urls import path
from .views import BrainTreeTokenGenerationView, BrainTreePaymentProcessingView


urlpatterns = [
    path('generate-braintree-token/', BrainTreeTokenGenerationView.as_view(), name='generate_token'),
    path('process-braintree-payment/', BrainTreePaymentProcessingView.as_view(), name='process_payment'),
]