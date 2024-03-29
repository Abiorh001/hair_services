from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import (
    ServiceProviderProfileSerializer,
    ServiceProviderAvailabilitySerializer,
    GetServiceProviderProfileSerializer,
    GetServiceProviderAvailabilitySerializer,
)
from .models import (
    ServiceProviderProfile,
    ServiceProviderAvailability,

)
from accounts.models import CustomUser
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.request import Request
from django.db import transaction
from appointment_booking.models import Appointment
from appointment_booking.serializers import ServiceProviderBookedAppointmentSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from utils.pagination import BasePagination
from service_categories.models import ServiceCategory
from service_categories.serializers import ServiceCategorySerializer
from datetime import datetime
from products.serializers import GetProductSerializer
from services.models import Service
from services.serializers import GetServiceSerializer, ServiceSerializer
from products.models import Product


class CreateServiceProviderProfileView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Create Service Provider Profile",
        operation_description="registered professional account can create service provider profile",
        tags=['Service Provider(Professional)'],
        request_body=ServiceProviderProfileSerializer,
        responses={
            201: ServiceProviderProfileSerializer(many=False),
            400: "Bad Request"
        }
    )
    def post(self, request: Request):
        user = request.user
        data = request.data
        data['user'] = user.id
        existing_user = CustomUser.objects.get(id=user.id)
        if existing_user.user_type != "professional":
            response = {
                "status": "failed",
                "message": "User is not a professional",
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        try:
            business_name = data.get('business_name').lower()
            data["business_name"] = business_name
            service_offered = data.get('service_offered')
            service_offered = ServiceCategory.objects.filter(category_name__in=service_offered)
            service_category_name = []
            for name in service_offered:
                service_category_name.append(name.id)
            data["service_offered"] = service_category_name
        except Exception:
            bad_request_response = {
                "status": "failed",
                "message": "all fields are required"
            }
            return Response(bad_request_response, status=status.HTTP_400_BAD_REQUEST)

        serializer = ServiceProviderProfileSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            response = {
                "status": "success",
                "message": "Service Provider Profile Created Successfully",
                "data": serializer.data
            }
            return Response(response, status=status.HTTP_201_CREATED)
        bad_request_response = {
            "success": "failed",
            "message": "Invalid Data",
            "data": serializer.errors
        }
        return Response(bad_request_response, status=status.HTTP_400_BAD_REQUEST)


class RetrieveUpdateServiceProviderProfileView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Retrieve Service Provider Profile",
        operation_description="registered professional account can retrieve their service provider profile",
        tags=['Service Provider(Professional)'],
        responses={
            200: GetServiceProviderProfileSerializer(many=True),
            404: "Not Found"
        }
    )
    def get(self, request: Request):
        try:
            user = request.user
            existing_user = CustomUser.objects.get(id=user.id)
            if existing_user.user_type != "professional":
                response = {
                    "status": "failed",
                    "message": "User is not a professional",
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            service_provider_profile = ServiceProviderProfile.objects.filter(user=user.id)
            serializer = GetServiceProviderProfileSerializer(service_provider_profile, many=True)
            response = {
                "status": "success",
                "message": "Service Provider Profile Retrieved Successfully",
                "data": serializer.data
            }
            return Response(response, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            response = {
                "status": "failed",
                "message": "User Does Not Exist"
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)
    
    @swagger_auto_schema(
        operation_summary="Update Service Provider Profile",
        operation_description="registered professional account can update their service provider profile",
        tags=['Service Provider(Professional)'],
        request_body=ServiceProviderProfileSerializer,
        responses={
            200: ServiceProviderProfileSerializer(many=False),
            400: "Bad Request",
            404: "Not Found"
        }
    )
    def patch(self, request: Request):
        try:
            user = request.user
            data = request.data
            existing_user = CustomUser.objects.get(id=user.id)
            if existing_user.user_type != "professional":
                response = {
                    "status": "failed",
                    "message": "User is not a professional",
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)

            if data.get("profile_picture"):
                data["profile_picture"] = request.FILES.get("profile_picture")
                service_provider_profile = ServiceProviderProfile.objects.get(user=user.id)
                serializer = ServiceProviderProfileSerializer(service_provider_profile, data=data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    response = {
                        "status": "success",
                        "message": "Service Provider Profile Updated Successfully",
                        "data": serializer.data
                    }
                    return Response(response, status=status.HTTP_200_OK)

            else:
                try:
                    business_name = data.get('business_name').lower()
                    data["business_name"] = business_name
                    service_offered = data.get('service_offered')
                    if service_offered:
                        service_offered = ServiceCategory.objects.filter(category_name__in=service_offered)
                        print(service_offered)
                        if not service_offered:
                            response = {
                                "status": "failed",
                                "message": "Service Category Does Not Exist",
                            }
                            return Response(response, status=status.HTTP_404_NOT_FOUND)
                        else:
                            service_category_name = [name.id for name in service_offered]
                            data["service_offered"] = service_category_name

                except Exception:
                    bad_request_response = {
                        "status": "failed",
                        "message": "all fields are required"
                    }
                    return Response(bad_request_response, status=status.HTTP_400_BAD_REQUEST)

                service_provider_profile = ServiceProviderProfile.objects.get(user=user.id)
                serializer = ServiceProviderProfileSerializer(service_provider_profile, data=data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    response = {
                        "status": "success",
                        "message": "Service Provider Profile Updated Successfully",
                        "data": serializer.data
                    }
                    return Response(response, status=status.HTTP_200_OK)
                else:
                    bad_request_response = {
                        "status": "failed",
                        "message": "Invalid Data",
                        "data": serializer.errors
                    }
                    return Response(bad_request_response, status=status.HTTP_400_BAD_REQUEST)

        except CustomUser.DoesNotExist:
            response = {
                "status": "failed",
                "message": "User Does Not Exist",
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)

        except ServiceProviderProfile.DoesNotExist:
            response = {
                "status": "failed",
                "message": "Service Provider Profile Does Not Exist",
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)


class ListServiceProviderServiceView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary="List Service Provider Services",
        operation_description="All users can view all service provider services",
        tags=['Service Provider(Professional)'],
        manual_parameters=[
            openapi.Parameter(
                name='business_name',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description='Business Name',
                required=True
            ),
        ],
        responses={
            200: GetServiceProviderProfileSerializer(many=True),
            404: "Not Found"
        }
    )
    def get(self, request: Request):
        try:
            business_name = request.query_params.get('business_name')
            service_provider_profile = ServiceProviderProfile.objects.get(business_name=business_name)
            service_provider_service = Service.objects.order_by('service_name').filter(service_provider=service_provider_profile)
            paginator = BasePagination()
            result_page = paginator.paginate_queryset(service_provider_service, request)
            serializer = GetServiceSerializer(result_page, many=True)
            response = {
                "status": "success",
                "message": "Service Provider Services Retrieved Successfully",
                "data": serializer.data
            }
            return paginator.get_paginated_response(response)
        except CustomUser.DoesNotExist:
            response = {
                "status": "failed",
                "message": "User Does Not Exist"
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        except ServiceProviderProfile.DoesNotExist:
            response = {
                "status": "failed",
                "message": "Service Provider Profile Does Not Exist",
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        except Service.DoesNotExist:
            response = {
                "status": "failed",
                "message": "Service Does Not Exist",
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        

class RetrieveUpdateDestroyServiceProviderServiceView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Retrieve Service Provider Service",
        operation_description="registered professional account can retrieve their service provider service",
        tags=['Service Provider(Professional)'],
        responses={
            200: GetServiceProviderProfileSerializer(many=True),
            404: "Not Found"
        }
    )
    def get(self, request: Request, id):
        try:
            user = request.user
            existing_user = CustomUser.objects.get(id=user.id)
            if existing_user.user_type != "professional":
                response = {
                    "status": "failed",
                    "message": "User is not a professional",
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            service_provider_profile = ServiceProviderProfile.objects.get(user=user.id)
            service_provider_service = Service.objects.filter(service_provider=service_provider_profile.id, id=id)
            if not service_provider_service:
                response = {
                    "status": "failed",
                    "message": "Service Does Not Exist",
                }
                return Response(response, status=status.HTTP_404_NOT_FOUND)
            serializer = GetServiceSerializer(service_provider_service, many=True)
            response = {
                "status": "success",
                "message": "Service Provider Service Retrieved Successfully",
                "data": serializer.data
            }
            return Response(response, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            response = {
                "status": "failed",
                "message": "User Does Not Exist"
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        except ServiceProviderProfile.DoesNotExist:
            response = {
                "status": "failed",
                "message": "Service Provider Profile Does Not Exist",
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        except Service.DoesNotExist:
            response = {
                "status": "failed",
                "message": "Service Does Not Exist",
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        operation_summary="Service Provider can update their Service by ID",
        operation_description="Service Provider can update any of their created Service by ID",
        tags=['Service Provider(Professional)'],
        request_body=ServiceSerializer,
        responses={
            200: ServiceSerializer,
            400: "Invalid Data",
            404: "Service Does Not Exist"
        }
    )
    def patch(self, request: Request, id):
        user = request.user
        try:
            service_provider = ServiceProviderProfile.objects.get(user=user)
        except ServiceProviderProfile.DoesNotExist:
            response = {
                "status": "failed",
                "message": "Service Provider Does Not Exist",
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        try:
            
            service = Service.objects.get(id=id, service_provider=service_provider)
            if not service:
                response = {
                    "status": "failed",
                    "message": "Service Does Not Exist",
                }
                return Response(response, status=status.HTTP_404_NOT_FOUND)
            data = request.data
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
            serializer = ServiceSerializer(service, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                response = {
                    "status": "success",
                    "message": "Service Updated Successfully",
                    "data": serializer.data
                }
                return Response(response, status=status.HTTP_200_OK)
            bad_request_response = {
                "success": "failed",
                "message": "Invalid Data",
                "data": serializer.errors
            }
            return Response(bad_request_response, status=status.HTTP_400_BAD_REQUEST)
        except Service.DoesNotExist:
            response = {
                "status": "failed",
                "message": "Service Does Not Exist"
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)
    
    @swagger_auto_schema(
        operation_summary="Delete Service Provider Service",
        operation_description="registered professional account can delete their service provider service",
        tags=['Service Provider(Professional)'],
        responses={
            204: "No Content",
            404: "Not Found"
        }
    )
    def delete(self, request: Request, id):
        try:
            user = request.user
            existing_user = CustomUser.objects.get(id=user.id)
            if existing_user.user_type != "professional":
                response = {
                    "status": "failed",
                    "message": "User is not a professional",
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            service_provider_profile = ServiceProviderProfile.objects.get(user=user.id)
            service_provider_service = Service.objects.filter(service_provider=service_provider_profile.id, id=id)
            if not service_provider_service:
                response = {
                    "status": "failed",
                    "message": "Service Does Not Exist",
                }
                return Response(response, status=status.HTTP_404_NOT_FOUND)
            service_provider_service.delete()
            response = {
                "status": "success",
                "message": "Service Provider Service Deleted Successfully",
            }
            return Response(response, status=status.HTTP_204_NO_CONTENT)
        except CustomUser.DoesNotExist:
            response = {
                "status": "failed",
                "message": "User Does Not Exist"
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        except ServiceProviderProfile.DoesNotExist:
            response = {
                "status": "failed",
                "message": "Service Provider Profile Does Not Exist",
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        except Service.DoesNotExist:
            response = {
                "status": "failed",
                "message": "Service Does Not Exist",
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)


class ServiceProviderSetAvailabityDayView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Set Service Provider Availability",
        operation_description="registered professional account can set their service provider availability",
        tags=['Service Provider(Professional)'],
        request_body=ServiceProviderAvailabilitySerializer,
        responses={
            201: ServiceProviderAvailabilitySerializer(many=False),
            400: "Bad Request"
        }
    )
    def post(self, request):
        data = request.data
        user = request.user
        data['user'] = user.id

        try:
            existing_user = CustomUser.objects.get(id=user.id)
            if existing_user.user_type != "professional":
                response = {
                    "status": "failed",
                    "message": "User is not a professional",
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)

            service_provider_profile = ServiceProviderProfile.objects.get(user=user.id)
            date_str = data.get('date')
            start_time_str = data.get('start_time')
            end_time_str = data.get('end_time')

            if date_str is None or start_time_str is None or end_time_str is None:
                response = {
                    "status": "failed",
                    "message": "Date, start time, and end time are required",
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)

            try:
                date = datetime.strptime(date_str, "%Y-%m-%d").date()
                start_time = datetime.strptime(start_time_str, "%H:%M:%S").time()
                end_time = datetime.strptime(end_time_str, "%H:%M:%S").time()
            except ValueError:
                response = {
                    "status": "failed",
                    "message": "Invalid date or time format",
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)

            if date < datetime.now().date():
                response = {
                    "status": "failed",
                    "message": "Invalid date. Date must be greater than or equal to today's date",
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            
            if start_time < datetime.now().time():
                response = {
                    "status": "failed",
                    "message": "Invalid time. Time must be greater than or equal to current time",
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            
            if start_time >= end_time:
                response = {
                    "status": "failed",
                    "message": "Start time must be less than end time",
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)

            # Check if there is existing availability for the same date
            existing_availability = ServiceProviderAvailability.objects.filter(
                service_provider=service_provider_profile,
                date=date
            ).first()

            # checking for overlapping time for the date
            if existing_availability:
                existing_time_ranges = ServiceProviderAvailability.objects.filter(
                    service_provider=service_provider_profile,
                    date=date
                    ).exclude(id=existing_availability.id)

                for existing_range in existing_time_ranges:
                    if not (end_time <= existing_range.start_time or start_time >= existing_range.end_time):
                        response = {
                            "status": "failed",
                            "message": "New time range overlaps with existing availability",
                            }
                        return Response(response, status=status.HTTP_400_BAD_REQUEST)


            # Create new availability
            data['service_provider'] = service_provider_profile.id
            print(data)
            serializer = ServiceProviderAvailabilitySerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                response = {
                    "status": "success",
                    "message": "Service Provider Availability Set Successfully",
                    "data": serializer.data
                }
                return Response(response, status=status.HTTP_201_CREATED)
            bad_request_response = {
                "success": "failed",
                "message": "Invalid Data",
                "data": serializer.errors
            }
            return Response(bad_request_response, status=status.HTTP_400_BAD_REQUEST)

        except CustomUser.DoesNotExist:
            response = {
                "status": "failed",
                "message": "User Does Not Exist",
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        except ServiceProviderProfile.DoesNotExist:
            response = {
                "status": "failed",
                "message": "Service Provider Profile Does Not Exist",
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            response = {
                "status": "failed",
                "message": str(e),
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ListServiceProviderProductsView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="List Service Provider Products",
        operation_description="registered professional account can list all their products",
        tags=['Service Provider(Professional)'],
        responses={
            200: GetProductSerializer(many=True),
            404: "Not Found"
        }
    )
    def get(self, request: Request):
        try:
            user = request.user
            existing_user = CustomUser.objects.get(id=user.id)
            if existing_user.user_type != "professional":
                response = {
                    "status": "failed",
                    "message": "User is not a professional",
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            service_provider_profile = ServiceProviderProfile.objects.get(user=user.id)
            service_provider_products = Product.objects.filter(owner=service_provider_profile).order_by('product_name')
            paginator = BasePagination()
            result_page = paginator.paginate_queryset(service_provider_products, request)
            serializer = GetProductSerializer(result_page, many=True)
            response = {
                "status": "success",
                "message": "Service Provider Products Retrieved Successfully",
                "data": serializer.data
            }
            return paginator.get_paginated_response(response)
        except CustomUser.DoesNotExist:
            response = {
                "status": "failed",
                "message": "User Does Not Exist"
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        except ServiceProviderProfile.DoesNotExist:
            response = {
                "status": "failed",
                "message": "Service Provider Profile Does Not Exist",
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        except Product.DoesNotExist:
            response = {
                "status": "failed",
                "message": "Product Does Not Exist",
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)


class ListServiceProviderAvailabilityView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary="List Service Provider Availability",
        operation_description="registered professional account can list all their service provider availability",
        tags=['Service Provider(Professional)'],
        manual_parameters=[
            openapi.Parameter(
                name='business_name',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description='Business Name',
                required=True
            ),
        ],
        responses={
            200: ServiceProviderAvailabilitySerializer(many=True),
            404: "Not Found"
        }
    )
    def get(self, request: Request):
        try:
            business_name = request.query_params.get('business_name')

            service_provider_profile = ServiceProviderProfile.objects.get(business_name=business_name)

            # Retrieve all ServiceProviderAvailability for the specific service provider
            service_provider_availability = ServiceProviderAvailability.objects.filter(
                service_provider=service_provider_profile.id
            )
            if not service_provider_availability:
                response = {
                    "status": "failed",
                    "message": "Service Provider Availability Does Not Exist",
                }
                return Response(response, status=status.HTTP_404_NOT_FOUND)

            paginator = BasePagination()
            result_page = paginator.paginate_queryset(service_provider_availability, request)
            serializer = GetServiceProviderAvailabilitySerializer(result_page, many=True)
            response = {
                "status": "success",
                "message": "Service Provider Availability Retrieved Successfully",
                "data": serializer.data
            }
            return paginator.get_paginated_response(response)
        except CustomUser.DoesNotExist:
            response = {
                "status": "failed",
                "message": "User Does Not Exist"
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND) 
        except ServiceProviderProfile.DoesNotExist:
            response = {
                "status": "failed",
                "message": "Service Provider Profile Does Not Exist",
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        except ServiceProviderAvailability.DoesNotExist:
            response = {
                "status": "failed",
                "message": "Service Provider Availability Does Not Exist",
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)


class ListServiceProviderAvailabilityByDateView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary="List specific Service Provider Availability Date and times available by business name",
        operation_description="All users can view specific service provider availability date and times available by business name",
        tags=['Service Provider(Professional)'],
        manual_parameters=[
            openapi.Parameter(
                name='business_name',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description='Business Name',
                required=True
            ),
            openapi.Parameter(
                name='date',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description='Date in YYYY-MM-DD format',
                required=True
            ),
        ],
        responses={
            200: ServiceProviderAvailabilitySerializer(many=True),
            404: "Not Found"
        }
    )
    def get(self, request: Request):
        try:
            business_name = request.query_params.get('business_name')
            date_str = request.query_params.get('date')
            if not business_name or not date_str:
                response = {
                    "status": "failed",
                    "message": "Both business_name, and date are required in the query parameters",
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)

            if business_name is not None and date_str is not None:
                business_name = business_name.lower()
                service_provider_profile = ServiceProviderProfile.objects.get(business_name=business_name)

                # Convert date string to datetime object
                date = datetime.strptime(date_str, '%Y-%m-%d').date()

                # Filter ServiceProviderAvailability based on the date within available_dates and available_times
                service_provider_availability = ServiceProviderAvailability.objects.filter(
                    service_provider=service_provider_profile.id,
                    date=date,

                )

                if service_provider_availability:
                    serializer = GetServiceProviderAvailabilitySerializer(service_provider_availability, many=True)
                    response = {
                        "status": "success",
                        "message": f"Service Provider {business_name} Availability Successfully retrieved for {date_str} ",
                        "data": serializer.data
                        
                    }
                    return Response(response, status=status.HTTP_200_OK)
                else:
                    response = {
                        "status": "failed",
                        "message": f"Service Provider is not available on {date_str}",
                    }
                    return Response(response, status=status.HTTP_404_NOT_FOUND)
                
        except ServiceProviderProfile.DoesNotExist:
            response = {
                "status": "failed",
                "message": "Service Provider Profile Does Not Exist",
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        except ServiceProviderAvailability.DoesNotExist:
            response = {
                "status": "failed",
                "message": "Service Provider Availability Does Not Exist",
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        

class RetrieveUpdateDestroyServiceProviderAvailabilityView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Retrieve Service Provider Availability",
        operation_description="registered professional account can retrieve their service provider availability",
        tags=['Service Provider(Professional)'],
        responses={
            200: ServiceProviderAvailabilitySerializer(many=True),
            404: "Not Found"
        }
    )
    def get(self, request: Request, id):
        try:
            user = request.user

            existing_user = CustomUser.objects.get(id=user.id)
            if existing_user.user_type != "professional":
                response = {
                    "status": "failed",
                    "message": "User is not a professional",
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)

            service_provider_profile = ServiceProviderProfile.objects.get(user=user.id)

            # Retrieve ServiceProviderAvailability for the specific date
            service_provider_availability = ServiceProviderAvailability.objects.filter(
                service_provider=service_provider_profile,
                id=id
            )
            if not service_provider_availability:
                response = {
                    "status": "failed",
                    "message": "Service Provider Availability Does Not Exist",
                }
                return Response(response, status=status.HTTP_404_NOT_FOUND)

            serializer = GetServiceProviderAvailabilitySerializer(service_provider_availability, many=True)
            response = {
                "status": "success",
                "message": "Service Provider Availability Retrieved Successfully",
                "data": serializer.data
            }
            return Response(response, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            response = {
                "status": "failed",
                "message": "User Does Not Exist"
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND) 
        except ServiceProviderProfile.DoesNotExist:
            response = {
                "status": "failed",
                "message": "Service Provider Profile Does Not Exist",
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        except ServiceProviderAvailability.DoesNotExist:
            response = {
                "status": "failed",
                "message": "Service Provider Availability Does Not Exist",
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        operation_summary="Update Service Provider Availability",
        operation_description="registered professional account can update their service provider availability",
        tags=['Service Provider(Professional)'],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'date': openapi.Schema(type=openapi.TYPE_STRING, description='Date in YYYY-MM-DD format'),
                'start_time': openapi.Schema(type=openapi.TYPE_STRING, description='Start Time in HH:MM:SS format'),
                'end_time': openapi.Schema(type=openapi.TYPE_STRING, description='End Time in HH:MM:SS format'),
            }
        ),
        responses={
            200: "Service Provider Availability Updated Successfully",
            400: "Bad Request",
            404: "Not Found"
        }
    )
    def patch(self, request, id):
        data = request.data
        user = request.user
        data['user'] = user.id

        try:
            existing_user = CustomUser.objects.get(id=user.id)
            if existing_user.user_type != "professional":
                response = {
                    "status": "failed",
                    "message": "User is not a professional",
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)

            service_provider_profile = ServiceProviderProfile.objects.get(user=user.id)
            date_str = data.get('date')
            start_time_str = data.get('start_time')
            end_time_str = data.get('end_time')

            if date_str is None or start_time_str is None or end_time_str is None:
                response = {
                    "status": "failed",
                    "message": "Date, start time, and end time are required",
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)

            try:
                date = datetime.strptime(date_str, "%Y-%m-%d").date()
                start_time = datetime.strptime(start_time_str, "%H:%M:%S").time()
                end_time = datetime.strptime(end_time_str, "%H:%M:%S").time()
            except ValueError:
                response = {
                    "status": "failed",
                    "message": "Invalid date or time format",
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)

            if date < datetime.now().date():
                response = {
                    "status": "failed",
                    "message": "Invalid date. Date must be greater than or equal to today's date",
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)

            if start_time < datetime.now().time():
                response = {
                    "status": "failed",
                    "message": "Invalid time. Time must be greater than or equal to the current time",
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)

            if start_time >= end_time:
                response = {
                    "status": "failed",
                    "message": "Start time must be less than end time",
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            

            # Check if there is existing availability for the same date
            existing_availability = ServiceProviderAvailability.objects.filter(
                service_provider=service_provider_profile,
                date=date,
                id=id
            ).first()
            
            # checking if no availability for the date
            if not existing_availability:
                response = {
                    "status": "failed",
                    "message": "Service Provider Availability Does Not Exist",
                }
                return Response(response, status=status.HTTP_404_NOT_FOUND)


            # checking for overlapping time for the date
            if existing_availability:
                existing_time_ranges = ServiceProviderAvailability.objects.filter(
                    service_provider=service_provider_profile,
                    date=date,
                ).exclude(id=existing_availability.id)

                for existing_range in existing_time_ranges:
                    if not (end_time <= existing_range.start_time or start_time >= existing_range.end_time):
                        response = {
                            "status": "failed",
                            "message": "New time range overlaps with existing availability",
                        }
                        return Response(response, status=status.HTTP_400_BAD_REQUEST)

            # Update existing availability
            serializer = ServiceProviderAvailabilitySerializer(existing_availability, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                response = {
                    "status": "success",
                    "message": "Service Provider Availability Updated Successfully",
                    "data": serializer.data
                }
                return Response(response, status=status.HTTP_200_OK)

            bad_request_response = {
                "status": "failed",
                "message": "Invalid Data",
                "data": serializer.errors
            }
            return Response(bad_request_response, status=status.HTTP_400_BAD_REQUEST)

        except CustomUser.DoesNotExist:
            response = {
                "status": "failed",
                "message": "User Does Not Exist",
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        except ServiceProviderProfile.DoesNotExist:
            response = {
                "status": "failed",
                "message": "Service Provider Profile Does Not Exist",
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            response = {
                "status": "failed",
                "message": str(e),
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)     
    
    @swagger_auto_schema(
        operation_summary="Delete Service Provider Availability",
        operation_description="registered professional account can delete their service provider availability",
        tags=['Service Provider(Professional)'],
        responses={
            200: "Service Provider Availability Deleted Successfully",
            404: "Not Found"
        }
    )
    def delete(self, request: Request, id):
        try:
            user = request.user
            existing_user = CustomUser.objects.get(id=user.id)
            if existing_user.user_type != "professional":
                response = {
                    "status": "failed",
                    "message": "User is not a professional",
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            service_provider_profile = ServiceProviderProfile.objects.get(user=user.id)
            service_provider_availability = ServiceProviderAvailability.objects.get(service_provider=service_provider_profile, id=id)
            if not service_provider_availability:
                response = {
                    "status": "failed",
                    "message": "Service Provider Availability Does Not Exist",
                }
                return Response(response, status=status.HTTP_404_NOT_FOUND)
            
            service_provider_availability.delete()
            response = {
                    "status": "success",
                    "message": "Service Provider Availability Deleted Successfully",
                }
            return Response(response, status=status.HTTP_204_NO_CONTENT)
            
        except CustomUser.DoesNotExist:
            response = {
                "status": "failed",
                "message": "User Does Not Exist"
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        except ServiceProviderProfile.DoesNotExist:
            response = {
                "status": "failed",
                "message": "Service Provider Profile Does Not Exist",
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        except ServiceProviderAvailability.DoesNotExist:
            response = {
                "status": "failed",
                "message": "Service Provider Availability Does Not Exist",
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)


class ServiceProviderAllBookedAppointmentsView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="View All Service Provider Booked Appointments",
        operation_description="registered professional account can view all their booked appointments",
        tags=['Service Provider(Professional)'],
        responses={
            200: ServiceProviderBookedAppointmentSerializer(many=True),
            404: "Not Found"
        }
    )
    def get(self, request: Request):
        try:
            user = request.user
            try:
                service_provider_profile = ServiceProviderProfile.objects.get(user=user.id)
            except ServiceProviderProfile.DoesNotExist:
                response = {
                    "status": "failed",
                    "message": "Service Provider Profile Does Not Exist",
                }
                return Response(response, status=status.HTTP_404_NOT_FOUND)
            booked_appointments = Appointment.objects.filter(service_provider=service_provider_profile.id).order_by('-created_at')
            paginator = BasePagination()
            result_page = paginator.paginate_queryset(booked_appointments, request)
            serializer = ServiceProviderBookedAppointmentSerializer(result_page, many=True)
            response = {
                "status": "success",
                "message": "Service Provider Booked Appointments Retrieved Successfully",
                "data": serializer.data
            }
            return paginator.get_paginated_response(response)
        except ServiceProviderProfile.DoesNotExist:
            response = {
                "status": "failed",
                "message": "Service Provider Profile Does Not Exist",
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)


class ServiceProviderViewBookedAppointmentByDateView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="View Service Provider Booked Appointments by Date",
        operation_description="registered professional account can view all their booked appointments by date",
        tags=['Service Provider(Professional)'],
        manual_parameters=[
            openapi.Parameter(
                name='date',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description='Date in YYYY-MM-DD format',
                required=True
            ),
        ],
        responses={
            200: ServiceProviderBookedAppointmentSerializer(many=True),
            404: "Not Found"
        }
    )
    def get(self, request: Request):
        try:
            user = request.user
            try:
                service_provider_profile = ServiceProviderProfile.objects.get(user=user.id)
            except ServiceProviderProfile.DoesNotExist:
                response = {
                    "status": "failed",
                    "message": "Service Provider Profile Does Not Exist",
                }
                return Response(response, status=status.HTTP_404_NOT_FOUND)
            date_str = request.query_params.get('date')
            if not date_str:
                response = {
                    "status": "failed",
                    "message": "Date is required in the query parameters",
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            date = datetime.strptime(date_str, "%Y-%m-%d").date()
            booked_appointments = Appointment.objects.filter(service_provider=service_provider_profile.id, date=date).order_by('-created_at')
            paginator = BasePagination()
            result_page = paginator.paginate_queryset(booked_appointments, request)
            serializer = ServiceProviderBookedAppointmentSerializer(result_page, many=True)
            response = {
                "status": "success",
                "message": "Service Provider Booked Appointments Retrieved Successfully",
                "data": serializer.data
            }
            return paginator.get_paginated_response(response)
        except ServiceProviderProfile.DoesNotExist:
            response = {
                "status": "failed",
                "message": "Service Provider Profile Does Not Exist",
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)


class ServiceProviderViewPastBookedAppointmentView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="View Past Service Provider Booked Appointments",
        operation_description="registered professional account can view all their past booked appointments",
        tags=['Service Provider(Professional)'],
        responses={
            200: ServiceProviderBookedAppointmentSerializer(many=True),
            404: "Not Found"
        }
    )
    def get(self, request: Request):
        try:
            user = request.user
            try:
                service_provider_profile = ServiceProviderProfile.objects.get(user=user.id)
            except ServiceProviderProfile.DoesNotExist:
                response = {
                    "status": "failed",
                    "message": "Service Provider Profile Does Not Exist",
                }
                return Response(response, status=status.HTTP_404_NOT_FOUND)
            booked_appointments = Appointment.objects.filter(service_provider=service_provider_profile.id, status="finished").order_by('-created_at')
            serializer = ServiceProviderBookedAppointmentSerializer(booked_appointments, many=True)
            response = {
                "status": "success",
                "message": "Past Service Provider Booked Appointments Retrieved Successfully",
                "data": serializer.data
            }
            return Response(response, status=status.HTTP_200_OK)
        except ServiceProviderProfile.DoesNotExist:
            response = {
                "status": "failed",
                "message": "Service Provider Profile Does Not Exist",
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)


class ServiceProviderViewUpcomingBookedAppointmentView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="View Upcoming Service Provider Booked Appointments",
        operation_description="registered professional account can view all their upcoming booked appointments",
        tags=['Service Provider(Professional)'],
        responses={
            200: ServiceProviderBookedAppointmentSerializer(many=True),
            404: "Not Found"
        }
    )
    def get(self, request: Request):
        try:
            user = request.user
            try:
                service_provider_profile = ServiceProviderProfile.objects.get(user=user.id)
            except ServiceProviderProfile.DoesNotExist:
                response = {
                    "status": "failed",
                    "message": "Service Provider Profile Does Not Exist",
                }
                return Response(response, status=status.HTTP_404_NOT_FOUND)
            status = ["on-process", "on-waiting"]
            booked_appointments = Appointment.objects.filter(service_provider=service_provider_profile.id, status__in=status).order_by('-created_at')
            paginator = BasePagination()
            result_page = paginator.paginate_queryset(booked_appointments, request)
            serializer = ServiceProviderBookedAppointmentSerializer(result_page, many=True)
            response = {
                "status": "success",
                "message": "Upcoming Service Provider Booked Appointments Retrieved Successfully",
                "data": serializer.data
            }
            return paginator.get_paginated_response(response)
        except ServiceProviderProfile.DoesNotExist:
            response = {
                "status": "failed",
                "message": "Service Provider Profile Does Not Exist",
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)


class ServiceProviderRetrievedSingleBookedAppointment(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="View Single Service Provider Booked Appointment",
        operation_description="registered professional account can view a single booked appointment",
        tags=['Service Provider(Professional)'],
        responses={
            200: ServiceProviderBookedAppointmentSerializer(many=True),
            404: "Not Found"
        }
    )
    def get(self, request: Request, id):
        try:
            user = request.user
            try:
                service_provider_profile = ServiceProviderProfile.objects.get(user=user.id)
            except ServiceProviderProfile.DoesNotExist:
                response = {
                    "status": "failed",
                    "message": "Service Provider Profile Does Not Exist",
                }
                return Response(response, status=status.HTTP_404_NOT_FOUND)
            booked_appointment = Appointment.objects.filter(service_provider=service_provider_profile.id, id=id)
            if not booked_appointment:
                response = {
                    "status": "failed",
                    "message": "Booked Appointment Does Not Exist",
                }
                return Response(response, status=status.HTTP_404_NOT_FOUND)
            appointment_instance = booked_appointment.first()

            service = appointment_instance.service
            time_of_service = service.duration_minutes
            
            # save the appointment to trigger the pre_save signal
            if appointment_instance.status == "on-waiting":
                appointment_instance.notes = "Time Estimation: 50 Minutes"
            elif appointment_instance.status == "on-process":
                appointment_instance.notes = f"On Process {time_of_service} Minutes"
            elif appointment_instance.status == "finished":
                appointment_instance.notes = "Appointment Finished"
            appointment_instance.save()
            serializer = ServiceProviderBookedAppointmentSerializer(booked_appointment, many=True)
            response = {
                "status": "success",
                "message": "Service Provider Booked Appointment Retrieved Successfully",
                "data": serializer.data
            }
            return Response(response, status=status.HTTP_200_OK)
        except ServiceProviderProfile.DoesNotExist:
            response = {
                "status": "failed",
                "message": "Service Provider Profile Does Not Exist",
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)
