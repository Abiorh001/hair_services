from rest_framework import serializers
from service_categories.serializers import ServiceCategorySerializer
from .models import Service
from professional_service_provider.serializers import GetServiceProviderProfileSerializer


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = "__all__"
        

class GetServiceSerializer(serializers.ModelSerializer):
    service_provider = GetServiceProviderProfileSerializer(read_only=True)
    service_category = ServiceCategorySerializer(read_only=True)
    
    
    class Meta:
        model = Service
        fields = ['id', 'service_provider', 'service_category', 'service_name', 'description',
                  'price', 'duration_minutes', 'service_picture', ]
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        service_picture = data.get('service_picture')
        price = data.get('price')
        if price is not None:
            data['price'] = f'£{price}'
        if service_picture is not None:
            data['service_picture'] = service_picture.split('?')[0]
        return data
    
    