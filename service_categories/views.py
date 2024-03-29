from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.request import Request
from rest_framework.permissions import AllowAny, IsAdminUser
from drf_yasg.utils import swagger_auto_schema
from utils.pagination import BasePagination
from .models import ServiceCategory
from .serializers import ServiceCategorySerializer


class CreateServiceCategoryView(APIView):
    permission_classes = [IsAdminUser]
    
    @swagger_auto_schema(
        operation_summary="Admin user can create Service Category",
        operation_description="Admin user can create Service Category",
        tags=['Services'],
        request_body=ServiceCategorySerializer,
        responses={
            201: ServiceCategorySerializer,
            400: "Invalid Data",
        }
    )
    def post(self, request: Request):
        
        data = request.data
        serializer = ServiceCategorySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            response = {
                "status": "success",
                "message": "Service Category Created Successfully",
                "data": serializer.data
            }
            return Response(response, status=status.HTTP_201_CREATED)
        bad_request_response = {
            "success": "failed",
            "message": "Invalid Data",
            "data": serializer.errors
        }
        return Response(bad_request_response, status=status.HTTP_400_BAD_REQUEST)


class ListServiceCategoryView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary="All user can retrieve all Service Categories",
        operation_description="All user can retrieve all Service Categories",
        tags=['Services'],
        responses={
            200: ServiceCategorySerializer,
        }
    )
    def get(self, request: Request):
        service_categories = ServiceCategory.objects.order_by('category_name')
        paginator = BasePagination()
        result_page = paginator.paginate_queryset(service_categories, request)
        serializer = ServiceCategorySerializer(result_page, many=True)
        response = {
            "status": "success",
            "message": "All Service Categories Retrieved Successfully",
            "data": serializer.data
        }
        return paginator.get_paginated_response(response)


class RetrieveServiceCategoryView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary="All user can retrieve Service Category by ID",
        operation_description="All user can retrieve Service Category by ID",
        tags=['Services'],
        responses={
            201: ServiceCategorySerializer,
            400: "Invalid Data",
            404: "User Does Not Exist"
        }
    )
    def get(self, request: Request, id):
        service_categorie = ServiceCategory.objects.filter(id=id)
        serializer = ServiceCategorySerializer(service_categorie, many=True)
        response = {
            "status": "success",
            "message": "Service Category Retrieved Successfully",
            "data": serializer.data
        }
        return Response(response, status=status.HTTP_200_OK)

