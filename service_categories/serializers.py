from rest_framework import serializers
from .models import ServiceCategory


class ServiceCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceCategory
        fields = ['id', 'category_name', 'service_category_picture']
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        service_category_picture = data.get('service_category_picture')
        if service_category_picture is not None:
            data['service_category_picture'] = service_category_picture.split('?')[0]
        return data