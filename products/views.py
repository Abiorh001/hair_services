from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from .models import *
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from professional_service_provider.models import ServiceProviderProfile
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from utils.pagination import BasePagination



class CreateProductCategoryView(APIView):
    permission_classes = [IsAdminUser]
    serializer_class = ProductCategorySerializer

    @swagger_auto_schema(
        operation_description="Admin can Create a new product category",
        operation_summary="Create a new product category",
        request_body=ProductCategorySerializer, 
        tags=['Products'],
        responses={201: ProductCategorySerializer(many=True)}
    )
    def post(self, request, format=None):
        data = request.data
        serializer = ProductCategorySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            response = {
                'status': 'success',
                'message': 'Product Category created successfully',
                'data': serializer.data
            }
            return Response(response, status=status.HTTP_201_CREATED)

        else:
            bad_response = {
                'status': 'failed',
                'message': 'Product Category creation failed',
                'data': serializer.errors
            }
            return Response(bad_response, status=status.HTTP_400_BAD_REQUEST)


class ListProductCategoryView(APIView):
    permission_classes = [AllowAny]
    serializer_class = ProductCategorySerializer

    @swagger_auto_schema(
        operation_description="all users can view all product categories",
        operation_summary="View all product categories",
        tags=['Products'],
        responses={200: ProductCategorySerializer(many=True)}
    )
    def get(self, request, format=None):
        product_categories = ProductCategory.objects.order_by('category_name')
        paginator = BasePagination()
        result_page = paginator.paginate_queryset(product_categories, request)
        serializer = ProductCategorySerializer(result_page, many=True)
        response = {
            'status': 'success',
            'message': 'All Product Categories retrieved successfully',
            'data': serializer.data
        }
        return paginator.get_paginated_response(response)


class CreateProductView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Service Provider can Create a new product",
        operation_summary="Create a new product",
        tags=['Products'],
        request_body=ProductSerializer, 
        responses={201: ProductSerializer(many=True)}
    )
    def post(self, request, format=None):
        data = request.data
        user = request.user
        
        try:
            service_provider = ServiceProviderProfile.objects.get(user=user)
        except ServiceProviderProfile.DoesNotExist:
            response = {
                'status': 'failed',
                'message': 'You are not a service provider',
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        data['owner'] = service_provider.id
        product_category = data.get('product_category')

        try:
            existing_product_category = ProductCategory.objects.get(category_name=product_category)
        except ProductCategory.DoesNotExist:
            response = {
                'status': 'failed',
                'message': 'Product Category does not exist',
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        data['product_category'] = existing_product_category.id
        
        serializer = ProductSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            response = {
                'status': 'success',
                'message': 'Product created successfully',
                'data': serializer.data
            }
            return Response(response, status=status.HTTP_201_CREATED)

        else:
            bad_response = {
                'status': 'failed',
                'message': 'Product creation failed',
                'data': serializer.errors
            }
            return Response(bad_response, status=status.HTTP_400_BAD_REQUEST)


class ListProductView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="all users can view all products",
        operation_summary="View all products",
        tags=['Products'],
        responses={200: GetProductSerializer(many=True)}
    )
    def get(self, request, format=None):
        products = Product.objects.order_by('product_name')
        paginator = BasePagination()
        result_page = paginator.paginate_queryset(products, request)
        serializer = GetProductSerializer(result_page, many=True)
        response = {
            'status': 'success',
            'message': 'All Products retrieved successfully',
            'data': serializer.data
        }
        return paginator.get_paginated_response(response)


class RetrieveProductsByNameView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="all users can view a product(s) by name",
        operation_summary="View a product(s) by name",
        tags=['Products'],
        responses={200: GetProductSerializer(many=True)}
    )
    def get(self, request, product_name):
        try:
            products = Product.objects.filter(product_name__icontains=product_name).order_by('product_name')
        except Product.DoesNotExist:
            response = {
                'status': 'failed',
                'message': 'Product does not exist',
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        paginator = BasePagination()
        result_page = paginator.paginate_queryset(products, request)
        serializer = GetProductSerializer(result_page, many=True)
        response = {
            'status': 'success',
            'message': 'Product retrieved successfully',
            'data': serializer.data
        }
        return paginator.get_paginated_response(response)
    
    
class RetrieveUpdateDestroyProductView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Service Provider can view a product",
        operation_summary="View a product",
        tags=['Products'],
        responses={200: ProductSerializer(many=True)}
    )
    def get(self, request, id):
        user = request.user
        try:
            exisiting_user = CustomUser.objects.get(id=user.id)
        except CustomUser.DoesNotExist:
            response = {
                'status': 'failed',
                'message': 'User does not exist',
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        service_provider = ServiceProviderProfile.objects.get(user=user)
        try:
            product = Product.objects.get(id=id, owner=service_provider)
        except Product.DoesNotExist:
            response = {
                'status': 'failed',
                'message': 'Product does not exist',
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        serializer = ProductSerializer(product)
        response = {
            'status': 'success',
            'message': 'Product retrieved successfully',
            'data': serializer.data
        }
        return Response(response, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(
        operation_description="Service Provider can update a product",
        operation_summary="Update a product",
        tags=['Products'],
        request_body=ProductSerializer, 
        responses={200: ProductSerializer(many=True)}
    )
    def patch(self, request, id):
        data = request.data
        user = request.user
        try:
            exisiting_user = CustomUser.objects.get(id=user.id)
        except CustomUser.DoesNotExist:
            response = {
                'status': 'failed',
                'message': 'User does not exist',
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        service_provider = ServiceProviderProfile.objects.get(user=user)
        try:
            product = Product.objects.get(id=id, owner=service_provider)
        except Product.DoesNotExist:
            response = {
                'status': 'failed',
                'message': 'Product does not exist',
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        if data.get('product_category'):
            product_category = data.get('product_category')
            try:
                existing_product_category = ProductCategory.objects.get(category_name=product_category)
            except ProductCategory.DoesNotExist:
                response = {
                    'status': 'failed',
                    'message': 'Product Category does not exist',
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            data['product_category'] = existing_product_category.id
        serializer = ProductSerializer(product, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            response = {
                'status': 'success',
                'message': 'Product updated successfully',
                'data': serializer.data
            }
            return Response(response, status=status.HTTP_200_OK)

        else:
            bad_response = {
                'status': 'failed',
                'message': 'Product update failed',
                'data': serializer.errors
            }
            return Response(bad_response, status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(
        operation_description="Service Provider can delete a product",
        operation_summary="Delete a product",
        tags=['Products'],
        responses={200: ProductSerializer(many=True)}
    )
    def delete(self, request, id):
        user = request.user
        try:
            exisiting_user = CustomUser.objects.get(id=user.id)
        except CustomUser.DoesNotExist:
            response = {
                'status': 'failed',
                'message': 'User does not exist',
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        service_provider = ServiceProviderProfile.objects.get(user=user)
        try:
            product = Product.objects.get(id=id, owner=service_provider)
        except Product.DoesNotExist:
            response = {
                'status': 'failed',
                'message': 'Product does not exist',
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        product.delete()
        response = {
            'status': 'success',
            'message': 'Product deleted successfully',
        }
        return Response(response, status=status.HTTP_200_OK)


class CreateProductOrderView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Authenticated User can create a new product order",
        operation_summary="Create a new product order",
        tags=['Products'],
        request_body=ProductOrderSerializer, 
        responses={201: ProductOrderSerializer(many=True)}
    )
    def post(self, request):
        data = request.data
        user = request.user
        data['user'] = user.id
        product_name = data.get('product_name')
        try:
            exisiting_product = Product.objects.get(product_name=product_name)
        except Product.DoesNotExist:
            response = {
                'status': 'failed',
                'message': 'Product does not exist',
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        data['product'] = exisiting_product.id
        quantity = data.get('quantity')
        if not quantity:
            response = {
                'status': 'failed',
                'message': 'Quantity is required',
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        if quantity < 1:
            response = {
                'status': 'failed',
                'message': 'Quantity must be greater than 0',
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        
        total_price = exisiting_product.price * quantity
        data['total_price'] = total_price
        serializer = ProductOrderSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            response = {
                'status': 'success',
                'message': 'Product Order created successfully',
                'data': serializer.data
            }
            return Response(response, status=status.HTTP_201_CREATED)

        else:
            bad_response = {
                'status': 'failed',
                'message': 'Product Order creation failed',
                'data': serializer.errors
            }
            return Response(bad_response, status=status.HTTP_400_BAD_REQUEST)


class ListProductOrderView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Authenticated User can view all its product orders",
        operation_summary="View all product orders",
        tags=['Products'],
        responses={200: GetProductOrderSerializer(many=True)}
    )
    def get(self, request):
        user = request.user
        product_orders = ProductOrder.objects.filter(user=user).order_by('-created_at')
        paginator = BasePagination()
        result_page = paginator.paginate_queryset(product_orders, request)
        serializer = GetProductOrderSerializer(result_page, many=True)
        response = {
            'status': 'success',
            'message': 'All Product Orders retrieved successfully',
            'data': serializer.data
        }
        return paginator.get_paginated_response(response)
    

class RetrieveUpdateDestroyProductOrderView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Authenticated User can view a product order",
        operation_summary="View a product order",
        tags=['Products'],
        responses={200: ProductOrderSerializer(many=True)}
    )
    def get(self, request, id):
        user = request.user
        try:
            product_order = ProductOrder.objects.get(id=id, user=user)
        except ProductOrder.DoesNotExist:
            response = {
                'status': 'failed',
                'message': 'Product Order does not exist',
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        serializer = GetProductOrderSerializer(product_order)
        response = {
            'status': 'success',
            'message': 'Product Order retrieved successfully',
            'data': serializer.data
        }
        return Response(response, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(
        operation_description="Authenticated User can update a product order",
        operation_summary="Update a product order",
        tags=['Products'],
        request_body=ProductOrderSerializer, 
        responses={200: ProductOrderSerializer(many=True)}
    )
    def patch(self, request, id):
        data = request.data
        user = request.user
        try:
            product_order = ProductOrder.objects.get(id=id, user=user)
        except ProductOrder.DoesNotExist:
            response = {
                'status': 'failed',
                'message': 'Product Order does not exist',
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        if data.get('quantity'):
            quantity = data.get('quantity')
            if quantity < 1:
                response = {
                    'status': 'failed',
                    'message': 'Quantity must be greater than 0',
                    }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            existing_product = product_order.product
            total_price = existing_product.price * quantity
            data['total_price'] = total_price
        serializer = ProductOrderSerializer(product_order, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            response = {
                'status': 'success',
                'message': 'Product Order updated successfully',
                'data': serializer.data
            }
            return Response(response, status=status.HTTP_200_OK)

        else:
            bad_response = {
                'status': 'failed',
                'message': 'Product Order update failed',
                'data': serializer.errors
            }
            return Response(bad_response, status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(
        operation_description="Authenticated User can delete a product order",
        operation_summary="Delete a product order",
        tags=['Products'],
        responses={200: ProductOrderSerializer(many=True)}
    )
    def delete(self, request, id):
        user = request.user
        try:
            product_order = ProductOrder.objects.get(id=id, user=user)
        except ProductOrder.DoesNotExist:
            response = {
                'status': 'failed',
                'message': 'Product Order does not exist',
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        product_order.delete()
        response = {
            'status': 'success',
            'message': 'Product Order deleted successfully',
        }
        return Response(response, status=status.HTTP_204_NO_CONTENT)
    
