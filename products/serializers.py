from accounts.models import CustomUser
from accounts.serializers import CustomUserSerializer, GetCustomUserSerializer
from .models import *
from rest_framework import serializers
from professional_service_provider.serializers import GetServiceProviderProfileSerializer



class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ['id', 'category_name', 'product_category_picture']
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        product_category_picture = data.get('product_category_picture')
        if product_category_picture is not None:
            data['product_category_picture'] = product_category_picture.split('?')[0]
        return data


class ProductSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'owner', 'product_category', 'product_name', 'description', 'price', 'product_picture']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        product_picture = data.get('product_picture')
        if product_picture is not None:
            data['product_picture'] = product_picture.split('?')[0]
        return data


class GetProductSerializer(serializers.ModelSerializer):
    owner = GetServiceProviderProfileSerializer(read_only=True)
    product_category = serializers.ReadOnlyField(source='product_category.category_name')
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'owner', 'product_category', 'product_name', 'description', 'price', 'product_picture']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        product_picture = data.get('product_picture')
        price = data.get('price')
        if price is not None:
            data['price'] = f'£{price}'
        if product_picture is not None:
            data['product_picture'] = product_picture.split('?')[0]
        return data

class ProductOrderSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = ProductOrder
        fields = ['id', 'user', 'product', 'quantity', 'total_price', 'order_status']


class GetProductOrderSerializer(serializers.ModelSerializer):
    user = GetCustomUserSerializer(read_only=True)
    product = ProductSerializer(read_only=True)
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = ProductOrder
        fields = ['id', 'user', 'product', 'quantity', 'total_price', 'order_status']