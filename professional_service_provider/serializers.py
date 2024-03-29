from rest_framework import serializers
from service_categories.serializers import ServiceCategorySerializer
from accounts.serializers import GetCustomUserSerializer
from .models import ServiceProviderProfile, ServiceProviderAvailability


class ServiceProviderProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceProviderProfile
        fields = ['id', 'user', 'business_name', 'business_description', 'business_address', 'city', 'state', 'postal_code', 'country',  'about_me', 'service_offered', 'profile_picture']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        profile_picture = data.get('profile_picture')
        business_picture = data.get('business_picture')
        if profile_picture is not None:
            data['profile_picture'] = profile_picture.split('?')[0]
        if business_picture is not None:
            data['business_picture'] = business_picture.split('?')[0]
        return data
    

class GetServiceProviderProfileSerializer(serializers.ModelSerializer):
    user = GetCustomUserSerializer(read_only=True)
    service_offered = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = ServiceProviderProfile
        fields = ['id', 'user', 'business_name', 'business_description', 'business_address', 'city', 'state', 'postal_code', 'country', 'about_me', 'service_offered', 'profile_picture']
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        profile_picture = data.get('profile_picture')
        if profile_picture is not None:
            data['profile_picture'] = profile_picture.split('?')[0]
        return data
    
    def get_service_offered(self, obj):
        return obj.service_offered.values_list('category_name', flat=True)


class ServiceProviderAvailabilitySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ServiceProviderAvailability
        fields = ['id', 'service_provider', 'date', 'start_time', 'end_time']


class GetServiceProviderAvailabilitySerializer(serializers.ModelSerializer):
    service_provider = GetServiceProviderProfileSerializer(read_only=True)
    
    class Meta:
        model = ServiceProviderAvailability
        fields = ['id', 'service_provider', 'date', 'start_time', 'end_time']

                  
class GetServiceProviderShopSerializer(serializers.ModelSerializer):

    class Meta:
        model = ServiceProviderProfile
        fields = ['business_name', 'business_description', 'business_address', 'city', 'state', 'postal_code', 'country', 'business_picture']
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        business_picture = data.get('business_picture')
        if business_picture is not None:
            data['business_picture'] = business_picture.split('?')[0]
        return data
    
   