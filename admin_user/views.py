from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from accounts.models import CustomUser
from .models import *
from .serializers import *
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.request import Request
from drf_yasg.utils import swagger_auto_schema
from accounts.serializers import GetCustomUserSerializer
from utils.pagination import BasePagination
from professional_service_provider.models import ServiceProviderProfile
from professional_service_provider.serializers import GetServiceProviderProfileSerializer
import datetime
from appointment_booking.models import Appointment
from appointment_booking.serializers import AppointmentSerializer
from .models import UserActivity
from .serializers import UserActivitySerializer


class AdminListAllUserView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="List of all users",
        operation_description="List of all users",
        tags=['Admin Management'],
        responses={
            200: GetCustomUserSerializer(many=True),
            400: "Bad Request"
        }
    )
    def get(self, request):
        user = request.user
        existing_user = get_object_or_404(CustomUser, id=user.id)
        if existing_user.user_type != 'admin':
            response = {
                "status": "forbidden",
                "message": "You are not authorized to perform this action",
            }
            return Response(response, status=status.HTTP_403_FORBIDDEN)
        users = CustomUser.objects.all().order_by('-created_at')
        paginator = BasePagination()
        result_page = paginator.paginate_queryset(users, request)
        serializer = GetCustomUserSerializer(result_page, many=True)
        response = {
            "status": "success",
            "message": "List of all users",
            "data": serializer.data
        }
        return paginator.get_paginated_response(response)


class AdminListAllClientView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="List of all clients",
        operation_description="List of all clients",
        tags=['Admin Management'],
        responses={
            200: GetCustomUserSerializer(many=True),
            400: "Bad Request"
        }
    )
    def get(self, request):
        user = request.user
        existing_user = get_object_or_404(CustomUser, id=user.id)
        if existing_user.user_type != 'admin':
            response = {
                "status": "forbidden",
                "message": "You are not authorized to perform this action",
            }
            return Response(response, status=status.HTTP_403_FORBIDDEN)
        clients = CustomUser.objects.filter(user_type='client').order_by('-created_at')
        paginator = BasePagination()
        result_page = paginator.paginate_queryset(clients, request)
        serializer = GetCustomUserSerializer(result_page, many=True)
        response = {
            "status": "success",
            "message": "List of all clients",
            "data": serializer.data
        }
        return paginator.get_paginated_response(response)


class AdminListAllProfessionalView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="List of all professionals",
        operation_description="List of all professionals",
        tags=['Admin Management'],
        responses={
            200: GetCustomUserSerializer(many=True),
            400: "Bad Request"
        }
    )
    def get(self, request):
        user = request.user
        existing_user = get_object_or_404(CustomUser, id=user.id)
        if existing_user.user_type != 'admin':
            response = {
                "status": "forbidden",
                "message": "You are not authorized to perform this action",
            }
            return Response(response, status=status.HTTP_403_FORBIDDEN)
        professionals = CustomUser.objects.filter(user_type='professional').order_by('-created_at')
        paginator = BasePagination()
        result_page = paginator.paginate_queryset(professionals, request)
        serializer = GetCustomUserSerializer(result_page, many=True)
        response = {
            "status": "success",
            "message": "List of all professionals",
            "data": serializer.data
        }
        return paginator.get_paginated_response(response)


class AdminListAllServiceProviderView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="List of all service providers",
        operation_description="List of all service providers",
        tags=['Admin Management'],
        responses={
            200: GetServiceProviderProfileSerializer(many=True),
            400: "Bad Request"
        }
    )
    def get(self, request):
        user = request.user
        existing_user = get_object_or_404(CustomUser, id=user.id)
        if existing_user.user_type != 'admin':
            response = {
                "status": "forbidden",
                "message": "You are not authorized to perform this action",
            }
            return Response(response, status=status.HTTP_403_FORBIDDEN)
        service_providers = ServiceProviderProfile.objects.all().order_by('-created_at')
        paginator = BasePagination()
        result_page = paginator.paginate_queryset(service_providers, request)
        serializer = GetServiceProviderProfileSerializer(result_page, many=True)
        response = {
            "status": "success",
            "message": "List of all service providers",
            "data": serializer.data
        }
        return paginator.get_paginated_response(response)

from service_categories.models import ServiceCategory
from professional_service_provider.serializers import ServiceProviderProfileSerializer
class CreateServiceProviderView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Create a service provider",
        operation_description="Create a service provider",
        tags=['Admin Management'],
        request_body=ServiceProviderProfileSerializer,
        responses={
            201: ServiceProviderProfileSerializer(),
            400: "Bad Request"
        }
    )
    def post(self, request):
        user = request.user
        data = request.data
        data['user'] = user.id
        existing_user = CustomUser.objects.get(id=user.id)
        if existing_user.user_type != "admin":
            response = {
                "status": "failed",
                "message": "User is not a admin",
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


class RetrieveUpdateDeleteServiceProviderView(APIView):
    @swagger_auto_schema(
        operation_summary="Retrieve a service provider",
        operation_description="Retrieve a service provider",
        tags=['Admin Management'],
        responses={
            200: GetServiceProviderProfileSerializer(),
            400: "Bad Request"
        }
    )
    def get(self, request, business_name):
        user = request.user
        existing_user = get_object_or_404(CustomUser, id=user.id)
        service_provider = get_object_or_404(ServiceProviderProfile, business_name=business_name)
        if existing_user.user_type != 'admin':
            response = {
                "status": "forbidden",
                "message": "You are not authorized to retrieve this service provider",
            }
            return Response(response, status=status.HTTP_403_FORBIDDEN)
        serializer = GetServiceProviderProfileSerializer(service_provider)
        response = {
            "status": "success",
            "message": "Service provider retrieved successfully",
            "data": serializer.data
        }
        return Response(response, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="admin can update a service provider",
        operation_description="admin can update a service provider",
        tags=['Admin Management'],
        request_body=ServiceProviderProfileSerializer,
        responses={
            200: GetServiceProviderProfileSerializer(),
            400: "Bad Request"
        }
    )
    def patch(self, request, business_name):
        user = request.user
        existing_user = get_object_or_404(CustomUser, id=user.id)
        service_provider = get_object_or_404(ServiceProviderProfile, business_name=business_name)
        if existing_user.user_type != 'admin':
            response = {
                "status": "forbidden",
                "message": "You are not authorized to update this service provider",
            }
            return Response(response, status=status.HTTP_403_FORBIDDEN)
        serializer = GetServiceProviderProfileSerializer(service_provider, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            response = {
                "status": "success",
                "message": "Service provider updated successfully",
                "data": serializer.data
            }
            return Response(response, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="delete a service provider",
        operation_description="delete a service provider",
        tags=['Admin Management'],
        responses={
            200: GetServiceProviderProfileSerializer(),
            400: "Bad Request"
        }
    )
    def delete(self, request, business_name):
        user = request.user
        existing_user = get_object_or_404(CustomUser, id=user.id)
        service_provider = get_object_or_404(ServiceProviderProfile, business_name=business_name)
        if existing_user.user_type != 'admin':
            response = {
                "status": "forbidden",
                "message": "You are not authorized to delete this service provider",
            }
            return Response(response, status=status.HTTP_403_FORBIDDEN)
        service_provider.delete()
        response = {
            "status": "success",
            "message": "Service provider deleted successfully",
        }
        return Response(response, status=status.HTTP_204_NO_CONTENT)

class AdminListNewUserView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="List of all new users for the current date and time",
        operation_description="List of all new users for the current date and time",
        tags=['Admin Management'],
        responses={
            200: GetCustomUserSerializer(many=True),
            400: "Bad Request"
        }
    )
    def get(self, request):
        user = request.user
        existing_user = get_object_or_404(CustomUser, id=user.id)
        if existing_user.user_type != 'admin':
            response = {
                "status": "forbidden",
                "message": "You are not authorized to perform this action",
            }
            return Response(response, status=status.HTTP_403_FORBIDDEN)
        new_users = CustomUser.objects.filter(created_at__date=datetime.date.today()).order_by('-created_at')
        paginator = BasePagination()
        result_page = paginator.paginate_queryset(new_users, request)
        serializer = GetCustomUserSerializer(result_page, many=True)
        response = {
            "status": "success",
            "message": f"List of all new users on {datetime.date.today()}",
            "data": serializer.data
        }
        return paginator.get_paginated_response(response)

from datetime import timedelta
from django.utils import timezone
class AdminListNewUserForTheWeek(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="List of all new users for  the week",
        operation_description="List of all new users for the week",
        tags=['Admin Management'],
        responses={
            200: GetCustomUserSerializer(many=True),
            400: "Bad Request"
        }
    )
    def get(self, request):
        user = request.user
        
        # Calculate the start of the week (7 days ago from the current date)
        start_of_week = timezone.now() - timedelta(days=7)
        
        existing_user = get_object_or_404(CustomUser, id=user.id)
        if existing_user.user_type != 'admin':
            response = {
                "status": "forbidden",
                "message": "You are not authorized to perform this action",
            }
            return Response(response, status=status.HTTP_403_FORBIDDEN)

        # Filter users created in the last week
        new_users = CustomUser.objects.filter(created_at__date__range=[start_of_week.date(), timezone.now().date()]).order_by('-created_at')
        paginator = BasePagination()
        result_page = paginator.paginate_queryset(new_users, request)
        serializer = GetCustomUserSerializer(result_page, many=True)
        response = {
            "status": "success",
            "message": "List of all new users for the week",
            "total_number": new_users.count(),
            "data": serializer.data
        }
        return paginator.get_paginated_response(response)


class AdminListAllAppointmentView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="List of all booked appointments",
        operation_description="List of all booked appointments",
        tags=['Admin Management'],
        responses={
            200: GetServiceProviderProfileSerializer(many=True),
            400: "Bad Request"
        }
    )
    def get(self, request):
        user = request.user
        existing_user = get_object_or_404(CustomUser, id=user.id)
        if existing_user.user_type != 'admin':
            response = {
                "status": "forbidden",
                "message": "You are not authorized to perform this action",
            }
            return Response(response, status=status.HTTP_403_FORBIDDEN)
        booked_appointments = Appointment.objects.all().order_by('-created_at')
        paginator = BasePagination()
        result_page = paginator.paginate_queryset(booked_appointments, request)
        serializer = AppointmentSerializer(result_page, many=True)
        response = {
            "status": "success",
            "message": "List of all booked appointments",
            "data": serializer.data
        }
        return paginator.get_paginated_response(response)


class AdminListAllNewBookedAppointmentView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="List of all new booked appointments",
        operation_description="List of all new booked appointments",
        tags=['Admin Management'],
        responses={
            200: GetServiceProviderProfileSerializer(many=True),
            400: "Bad Request"
        }
    )
    def get(self, request):
        user = request.user
        existing_user = get_object_or_404(CustomUser, id=user.id)
        if existing_user.user_type != 'admin':
            response = {
                "status": "forbidden",
                "message": "You are not authorized to perform this action",
            }
            return Response(response, status=status.HTTP_403_FORBIDDEN)
        from datetime import datetime
        

        current_date = datetime.now().date()  # Get the current date
        new_booked_appointments = Appointment.objects.filter(created_at__date=current_date).order_by('-created_at')
        paginator = BasePagination()
        result_page = paginator.paginate_queryset(new_booked_appointments, request)
        serializer = AppointmentSerializer(result_page, many=True)
        response = {
            "status": "success",
            "message": "List of all new booked appointments",
            "total_number": new_booked_appointments.count(),
            "data": serializer.data
        }
        return paginator.get_paginated_response(response)


class AdminListAllCompletedAppointmentView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="List of all completed appointments",
        operation_description="List of all completed appointments",
        tags=['Admin Management'],
        responses={
            200: GetServiceProviderProfileSerializer(many=True),
            400: "Bad Request"
        }
    )
    def get(self, request):
        user = request.user
        existing_user = get_object_or_404(CustomUser, id=user.id)
        if existing_user.user_type != 'admin':
            response = {
                "status": "forbidden",
                "message": "You are not authorized to perform this action",
            }
            return Response(response, status=status.HTTP_403_FORBIDDEN)
        completed_appointments = Appointment.objects.filter(status='finished').order_by('-created_at')
        paginator = BasePagination()
        result_page = paginator.paginate_queryset(completed_appointments, request)
        serializer = AppointmentSerializer(result_page, many=True)
        response = {
            "status": "success",
            "message": "List of all completed appointments",
            "data": serializer.data
        }
        return paginator.get_paginated_response(response)
    

class UserActivityView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="List of all user activities",
        operation_description="List of all user activities",
        tags=['Admin Management'],
        responses={
            200: UserActivitySerializer(many=True),
            400: "Bad Request"
        }
    )
    def get(self, request):
        user = request.user
        existing_user = get_object_or_404(CustomUser, id=user.id)
        if existing_user.user_type != "admin":
            response = {
                "status": "forbidden",
                "message": "You are not authorized to perform this action",
            }
            return Response(response, status=status.HTTP_403_FORBIDDEN)
        activities = UserActivity.objects.all().order_by('-created_at')
        paginator = BasePagination()
        result_page = paginator.paginate_queryset(activities, request)
        serializer = UserActivitySerializer(result_page, many=True)
        response = {
            "status": "success",
            "message": "List of all user activities",
            "data": serializer.data
        }
        return paginator.get_paginated_response(response)