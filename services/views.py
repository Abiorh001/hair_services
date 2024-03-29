from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from professional_service_provider.serializers import *
from professional_service_provider.models import ServiceProviderProfile
from .models import Service, ServiceCategory
from accounts.models import CustomUser
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.request import Request
from django.db.models import Q
from datetime import datetime
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from utils.pagination import BasePagination
from professional_service_provider.models import (
    ServiceProviderAvailability,
)
from recently_visited_page_middleware.utils import get_recently_visited_urls
from utils.average_rating import get_average_rating


class ListServiceView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary="Service Provider, guest, client or admin can retrieve all Services",
        operation_description="Service Provider, client or admin can retrieve all Services",
        tags=['Services'],
        responses={
            200: GetServiceSerializer,
        }
    )
    def get(self, request: Request):
        services = Service.objects.order_by('service_name')
        paginator = BasePagination()
        result_page = paginator.paginate_queryset(services, request)
        serializer = GetServiceSerializer(result_page, many=True)
        response = {
            "status": "success",
            "message": "All Services Retrieved Successfully",
            "data": serializer.data
        }
        return paginator.get_paginated_response(response)


class CreateServiceView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Service Provider can create Service",
        operation_description="Registered professional user as a Service Provider can create Service",
        tags=['Services'],
        request_body=ServiceSerializer,
        responses={
            201: ServiceSerializer,
            400: "Invalid Data",
            404: "User Does Not Exist"
        }
    )
    def post(self, request: Request):
        user = request.user

        try:
            data = request.data
            user = CustomUser.objects.get(id=user.id)

            try:
                service_name = data.get('service_name')
                service_provider = ServiceProviderProfile.objects.get(user=user)
                service = Service.objects.filter(service_name=service_name, service_provider=service_provider).first()

                if service is not None:
                    response = {
                        "status": "failed",
                        "message": "Service Already Exist",
                    }
                    return Response(response, status=status.HTTP_400_BAD_REQUEST)
                
                data['service_provider'] = service_provider.id
                service_category = data.get('service_category')

                try:
                    service_category = ServiceCategory.objects.get(category_name=service_category)
                except ServiceCategory.DoesNotExist:
                    response = {
                        "status": "failed",
                        "message": "Service Category Does Not Exist",
                    }
                    return Response(response, status=status.HTTP_404_NOT_FOUND)

                data['service_category'] = service_category.id
                serializer = ServiceSerializer(data=data)

                if serializer.is_valid():
                    serializer.save()
                    response = {
                        "status": "success",
                        "message": "Service Created Successfully",
                        "data": serializer.data
                    }
                    return Response(response, status=status.HTTP_201_CREATED)

                bad_request_response = {
                    "success": "failed",
                    "message": "Invalid Data",
                    "data": serializer.errors
                }
                return Response(bad_request_response, status=status.HTTP_400_BAD_REQUEST)

            except ServiceProviderProfile.DoesNotExist:
                response = {
                    "status": "failed",
                    "message": "Service Provider Does Not Exist",
                }
                return Response(response, status=status.HTTP_404_NOT_FOUND)

        except CustomUser.DoesNotExist:
            response = {
                "status": "failed",
                "message": "User Does Not Exist",
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)


class RecentlyVisitedPagesView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Authenticated User can Retrieve Recently Visited Pages",
        operation_description="Authenticated User Retrieve Recently Visited Pages",
        tags=['Services'],
        responses={
            200: 'List of Recently Visited Pages',
        }
    )
    def get(self, request):
        user_id = request.user.id

        recently_visited_urls = get_recently_visited_urls(user_id)

        response_data = {
            "status": "success",
            "message": "Recently Visited Pages Retrieved Successfully",
            "data": recently_visited_urls
        }

        return Response(response_data, status=status.HTTP_200_OK)


class RetrieveServiceView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary="Service Provider, guest,client or admin can retrieve Service by ID",
        operation_description="Service Provider, guest, client or admin can retrieve Service by ID",
        tags=['Services'],
        responses={
            200: GetServiceSerializer,
            400: "Invalid Data",
            404: "Service Does Not Exist"
        }
    )
    def get(self, request: Request, id):
        try:
            service = Service.objects.filter(id=id)
            serializer = GetServiceSerializer(service, many=True)
            response = {
                "status": "success",
                "message": "Service Retrieved Successfully",
                "data": serializer.data
            }
            return Response(response, status=status.HTTP_200_OK)
        except Service.DoesNotExist:
            response = {
                "status": "failed",
                "message": "Service Does Not Exist",
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)

    
class SearchListServiceProviderByService(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary="Any user can retrieve all professionals by Service",
        operation_description="Any user can retrieve all professionals by Service",
        tags=['Services'],
        manual_parameters=[
            openapi.Parameter(
                name='service',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description='Service Name',
                required=True,
            ),
        ],
        responses={
            200: GetServiceProviderProfileSerializer,
            400: "Invalid Data",
            404: "Service Does Not Exist"
        }
    )
    def get(self, request):
        service_name = request.query_params.get('service')

        # Filter services by service category
        if service_name:
            try:
                service = Service.objects.filter(service_name=service_name).first()
                if not service:
                    response = {
                        "status": "failed",
                        "message": "Service Does Not Exist",
                    }
                    return Response(response, status=status.HTTP_404_NOT_FOUND)
                service_category = service.service_category
                # check if service provider offer
                service_provider = ServiceProviderProfile.objects.filter(service_offered=service_category).order_by('business_name')
            except Service.DoesNotExist:
                response = {
                    "status": "failed",
                    "message": "Service Does Not Exist",
                }
                return Response(response, status=status.HTTP_404_NOT_FOUND)

        paginator = BasePagination()
        result_page = paginator.paginate_queryset(service_provider, request)
        serializer = GetServiceProviderProfileSerializer(result_page, many=True)
        response = {
            "status": "success",
            "message": "All Service providers Retrieved Successfully",
            "data": serializer.data
        }
        return paginator.get_paginated_response(response)


class SearchListServiceByCategoryAndLocationView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary="Any user can retrieve all professionals by Service Category and professionals Location",
        operation_description="Any user can retrieve all professionals by Service Category and professionals Location",
        tags=['Services'],
        manual_parameters=[
            openapi.Parameter(
                name='category',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description='Service Category Name',
                required=False,
            ),
            openapi.Parameter(
                name='location',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description='Service Provider Location',
                required=False,
            ),
        ],
        responses={
            200: GetServiceProviderProfileSerializer,
            400: "Invalid Data",
            404: "Service Category Does Not Exist"
        }
    )
    def get(self, request):
        service_category_name = request.query_params.get('category')
        location = request.query_params.get('location')

        # Filter services by service category
        if service_category_name:
            try:
                service_category = ServiceCategory.objects.get(category_name__iexact=service_category_name)
                services = Service.objects.filter(service_category=service_category).order_by('service_name')
                service_provider = ServiceProviderProfile.objects.filter(service__in=services)
            except ServiceCategory.DoesNotExist:
                response = {
                    "status": "failed",
                    "message": "Service Category Does Not Exist",
                }
                return Response(response, status=status.HTTP_404_NOT_FOUND)

        
        # If location is provided, filter services by city
        elif location:
            service_provider = ServiceProviderProfile.objects.filter(city__iexact=location)
            #services = services.filter(service_provider__in=service_provider).order_by('service_name')
        
        paginator = BasePagination()
        result_page = paginator.paginate_queryset(service_provider, request)

        serializer = GetServiceProviderProfileSerializer(result_page, many=True)

        response = {
            "status": "success",
            "message": "All Service providers Retrieved Successfully",
            "data": serializer.data
        }
        
        return paginator.get_paginated_response(response)


class SearchListServiceByCategory(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary="Any user can retrieve all services by Service Category",
        operation_description="Any user can retrieve all services by Service Category",
        tags=['Services'],
        manual_parameters=[
            openapi.Parameter(
                name='category',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description='Service Category Name',
                required=True,
            ),
        ],
        responses={
            200: GetServiceSerializer,
            400: "Invalid Data",
            404: "Service Category Does Not Exist"
        }
    )
    def get(self, request):
        service_category_name = request.query_params.get('category')

        # Filter services by service category
        if service_category_name:
            try:
                service_category = ServiceCategory.objects.get(category_name__iexact=service_category_name)
                services = Service.objects.filter(service_category=service_category).order_by('service_name')

            except ServiceCategory.DoesNotExist:
                response = {
                    "status": "failed",
                    "message": "Service Category Does Not Exist",
                }
                return Response(response, status=status.HTTP_404_NOT_FOUND)

        paginator = BasePagination()
        result_page = paginator.paginate_queryset(services, request)

        serializer = GetServiceSerializer(result_page, many=True)

        response = {
            "status": "success",
            "message": "All Services Retrieved  Successfully by service category",
            "data": serializer.data
        }
        
        return paginator.get_paginated_response(response)

class SearchListServiceByDateTimeAndLocationView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary="All Users can retrieve all Services by date, time and service provider Location",
        operation_description="All users can retrieve all Services by date, time and service provider Location",
        tags=['Services'],
        manual_parameters=[
            openapi.Parameter(
                name='date',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description='Date of Service',
                required=True,
            ),
            openapi.Parameter(
                name='time',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description='Time of Service',
                required=False,
            ),
            openapi.Parameter(
                name='location',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description='Service Provider Location',
                required=False,
            ),
        ],
        responses={
            200: GetServiceSerializer,
            400: "Invalid Data",
            404: "Service Does Not Exist"
        }
    )
    def get(self, request):
        user_date = request.query_params.get('date')
        time = request.query_params.get('time')
        location = request.query_params.get('location')

        # Parse the user-input date to a datetime object
        try:
            parsed_date = datetime.strptime(user_date, '%Y-%m-%d').date()
        except ValueError:
            response = {
                "status": "failed",
                "message": "Invalid date format. Use 'yyyy-mm-dd'.",
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        # Filter services by service availability date
        available_dates = ServiceProviderAvailableDate.objects.filter(date=parsed_date)
        if not available_dates.exists():
            response = {
                "status": "failed",
                "message": "Service is not available on this date",
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        services = ServiceProviderAvailability.objects.filter(available_dates__in=available_dates)
        print(services)

        # Filter services by time (uncomment and adjust as needed)
        # services = services.filter(Q(start_time__lte=time) & Q(end_time__gte=time))

        # If location is provided, filter services by city
        if location:
            services = services.filter(service_provider__city__iexact=location)
        paginator = BasePagination()
        result_page = paginator.paginate_queryset(services, request)
        serializer = GetServiceSerializer(result_page, many=True)

        response = {
            "status": "success",
            "message": "All Services Retrieved Successfully",
            "data": serializer.data
        }

        return paginator.get_paginated_response(response)


class ListAllServiceProvidersView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary="All users can retrieve all Service Providers profile",
        operation_description="All users can retrieve all Service Providers profile",
        tags=['Services'],
        responses={
            200: GetServiceProviderProfileSerializer,
        }
    )
    def get(self, request):
        service_providers = ServiceProviderProfile.objects.order_by('business_name')
        # for business_name in service_providers:
        #     average_rating = get_average_rating(business_name)
            
        paginator = BasePagination()
        result_page = paginator.paginate_queryset(service_providers, request)
        serializer = GetServiceProviderProfileSerializer(result_page, many=True)

        

        response = {
            "status": "success",
            "message": "All Service Providers Retrieved Successfully",
            "data": serializer.data
        }
        return paginator.get_paginated_response(response)


class RetrieveServiceProviderView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary="All users can retrieve Service Provider profile by business name",
        operation_description="All users can retrieve Service Provider profile by business name",
        tags=['Services'],
        manual_parameters=[
            openapi.Parameter(
                name='business_name',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description='Service Provider Business Name',
                required=True,
            ),
        ],
        responses={
            200: GetServiceProviderProfileSerializer,
            400: "Invalid Data",
            404: "Service Provider Does Not Exist"
        }
    )
    def get(self, request: Request):
        try:
            business_name = request.query_params.get('business_name')
            
            service_provider = ServiceProviderProfile.objects.filter(business_name=business_name)
            if not service_provider:
                response = {
                    "status": "failed",
                    "message": "Service Provider Does Not Exist",
                }
                return Response(response, status=status.HTTP_404_NOT_FOUND)
            serializer = GetServiceProviderProfileSerializer(service_provider)
            response = {
                "status": "success",
                "message": "Service Provider Retrieved Successfully",
                "data": serializer.data
            }
            return Response(response, status=status.HTTP_200_OK)
        except ServiceProviderProfile.DoesNotExist:
            response = {
                "status": "failed",
                "message": "Service Provider Does Not Exist",
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)


class ListAllserviceProviderServices(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary="All users can retrieve all Services of a service provider",
        operation_description="All users can retrieve all Services of a service provider",
        tags=['Services'],
        manual_parameters=[
            openapi.Parameter(
                name='business_name',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description='Service Provider Business Name',
                required=True,
            ),
        ],
        responses={
            200: GetServiceSerializer,
        }
    )
    def get(self, request):
        service_provider = request.query_params.get('business_name')
        service_provider = ServiceProviderProfile.objects.filter(business_name=service_provider).first()
        if service_provider is None:
            response = {
                "status": "failed",
                "message": "Service Provider Does Not Exist",
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        services = Service.objects.filter(service_provider=service_provider).order_by('service_name')
        paginator = BasePagination()
        result_page = paginator.paginate_queryset(services, request)
        serializer = GetServiceSerializer(result_page, many=True)
        response = {
            "status": "success",
            "message": f"All services retrieved successfully for {service_provider}",
            "data": serializer.data
        }
        return paginator.get_paginated_response(response)


class ListAllServiceProviderShopView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary="All users can retrieve all Service Providers Shops",
        operation_description="All users can retrieve all Service Providers Shops",
        tags=['Services'],
        responses={
            200: GetServiceProviderShopSerializer,
        }
    )
    def get(self, request):
        service_providers = ServiceProviderProfile.objects.order_by('business_name')
        paginator = BasePagination()
        result_page = paginator.paginate_queryset(service_providers, request)
        serializer = GetServiceProviderShopSerializer(result_page, many=True)
        response = {
            "status": "success",
            "message": "All Service Providers Shops Retrieved Successfully",
            "data": serializer.data
        }
        return paginator.get_paginated_response(response)


class RetrieveServiceProviderShopView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary="All users can retrieve Service Provider Shop by business name",
        operation_description="All users can retrieve Service Provider Shop by business name",
        tags=['Services'],
        manual_parameters=[
            openapi.Parameter(
                name='business_name',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description='Service Provider Business Name',
                required=True,
            ),
        ],
        responses={
            200: GetServiceProviderShopSerializer,
            400: "Invalid Data",
            404: "Service Provider Shop Does Not Exist"
        }
    )
    def get(self, request: Request):
        business_name = request.query_params.get('business_name')
        try:
            service_provider = ServiceProviderProfile.objects.get(business_name=business_name)
    
            serializer = GetServiceProviderShopSerializer(service_provider)
            response = {
                "status": "success",
                "message": "Service Provider Shop Retrieved Successfully",
                "data": serializer.data
            }
            return Response(response, status=status.HTTP_200_OK)
        except ServiceProviderProfile.DoesNotExist:
            response = {
                "status": "failed",
                "message": "Service Provider Shop Does Not Exist",
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)


class ListOfFeaturedServiceProvidersViews(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary="All users can retrieve all featured Service Providers",
        operation_description="All users can retrieve all featured Service Providers",
        tags=['Services'],
        responses={
            200: GetServiceProviderProfileSerializer,
        }
    )
    def get(self, request):
        service_providers = ServiceProviderProfile.objects.filter(service_provider_subscription='premium').order_by('-created_at')
        paginator = BasePagination()
        result_page = paginator.paginate_queryset(service_providers, request)
        serializer = GetServiceProviderProfileSerializer(result_page, many=True)
        response = {
            "status": "success",
            "message": "All Featured Service Providers Retrieved Successfully",
            "data": serializer.data
        }
        return paginator.get_paginated_response(response)

from review_and_rating.models import ReviewAndRating
from django.db.models import Sum
class ListOfTopRatedServiceProvidersViews(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary="All users can retrieve all top rated Service Providers",
        operation_description="All users can retrieve all top rated Service Providers",
        tags=['Services'],
        responses={
            200: GetServiceProviderProfileSerializer,
        }
    )
    def get(self, request):
        service_providers_rating = ReviewAndRating.objects.values('service_provider').annotate(total_sum=Sum('rating')).order_by('-total_sum')
        service_providers = []
        for service_provider_rating in service_providers_rating:
            service_provider = ServiceProviderProfile.objects.get(id=service_provider_rating['service_provider'])
            service_providers.append(service_provider)
        paginator = BasePagination()
        result_page = paginator.paginate_queryset(service_providers, request)
        serializer = GetServiceProviderProfileSerializer(result_page, many=True)
        response = {
            "status": "success",
            "message": "All Top Rated Service Providers Retrieved Successfully",
            "data": serializer.data
        }
        return paginator.get_paginated_response(response)