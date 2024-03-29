from rest_framework import serializers
from .models import ServiceProviderServicesTransaction, ServiceProviderProductsTransaction


class ServiceProviderServicesTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceProviderServicesTransaction
        fields = '__all__'


class ServiceProviderProductsTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceProviderProductsTransaction
        fields = '__all__'