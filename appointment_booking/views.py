from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from professional_service_provider.serializers import *
from .models import *
from services.models import Service
from .serializers import *
from accounts.models import CustomUser
from professional_service_provider.models import ServiceProviderProfile
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from datetime import datetime
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from professional_service_provider.models import ServiceProviderAvailability
from django.utils import timezone
from utils.pagination import BasePagination
from datetime import datetime, timedelta
from service_categories.models import ServiceCategory


class UserBookedAppointmentView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Book an appointment",
        operation_description="Book an appointment",
        tags=['Appointment'],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'time': openapi.Schema(type=openapi.TYPE_STRING),
                'date': openapi.Schema(type=openapi.TYPE_STRING),
                'service_provider': openapi.Schema(type=openapi.TYPE_STRING),
                'service': openapi.Schema(type=openapi.TYPE_STRING),
            }
        ),
        responses={
            201: AppointmentSerializer(),
            400: "Bad Request"
        }
    )
    def post(self, request):
        user = request.user
        data = request.data
        time = data.get('time')
        date = data.get('date')
        service_provider_name = data.get('service_provider')
        service_name = data.get('service')
        
        try:
            service_provider = ServiceProviderProfile.objects.get(business_name__iexact=service_provider_name)
            service = Service.objects.get(service_name__iexact=service_name, service_provider=service_provider)
            
        except ServiceProviderProfile.DoesNotExist:
            response = {
                "status": "error",
                "message": "Service provider does not exist"
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        except Service.DoesNotExist:
            response = {
                "status": "error",
                "message": "Service does not exist"
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        # Validate date and time format
        try:
            datetime.strptime(date, "%Y-%m-%d")
            datetime.strptime(time, "%H:%M:%S")
        except ValueError:
            response = {
                "status": "error",
                "message": "Invalid date or time format"
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        # Convert date and time strings to timezone-aware datetime objects
        datetime_now = timezone.now()
        date = timezone.datetime.strptime(date, "%Y-%m-%d").date()
        time = timezone.datetime.strptime(time, "%H:%M:%S").time()

        # Check if the date is in the past
        if date < datetime_now.date():
            response = {
                    "status": "error", 
                    "message": "Date provided is in the past"
                    }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        # Check if the time is in the past
        if date == datetime_now.date() and time < datetime_now.time():
            response = {
                    "status": "error", 
                    "message": "Time provided is in the past"
                    }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        # Check if the service provider is available on the given date
        
        availability_date = ServiceProviderAvailability.objects.filter(
            date=date,
            service_provider=service_provider,
            start_time__lte=time,
            end_time__gte=time
        ).first()
    
        if not availability_date:
            response = {
                "status": "error",
                "message": "Service provider is not available at the given date"
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        # Check if the time is already booked
        if Appointment.objects.filter(
            service_provider=service_provider,
            service=service,
            date=date,
            time=time
        ).exists():
            response = {
                "status": "error",
                "message": "Service provider has already been booked for this time"
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        # Check if the specified time falls within the available time slots
        start_time = availability_date.start_time
        end_time = availability_date.end_time

        if not (start_time <= time <= end_time):
            response = {
                "status": "error",
                "message": "Service provider is not available at the given time"
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        # getting the service duration
        service_duration = timedelta(minutes=service.duration_minutes)

        # Check if there is enough time remaining for the service
        datetime_now = datetime.now()
        appointment_datetime = datetime(datetime_now.year, datetime_now.month, datetime_now.day, time.hour, time.minute, time.second)

        if appointment_datetime + service_duration > datetime(datetime_now.year, datetime_now.month, datetime_now.day, end_time.hour, end_time.minute, end_time.second):
            response = {
                "status": "error",
                "message": "Not enough time available for the selected service"
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        # Create an Appointment object
        appointment = Appointment(
            user=user,
            service_provider=service_provider,
            service=service,
            date=date,
            time=time,
            status="booked"
        )
        appointment.save()

        # Create an AppointmentCheckout object
        appointment_checkout = AppointmentCheckout(
            appointment=appointment,
            total_price=service.price,
            payment_status="pending",
            payment_method="cash"
        )
        appointment_checkout.save()

        serializer = AppointmentSerializer(appointment)

        response = {
            "status": "success",
            "message": "Appointment booked successfully",
            "data": serializer.data
        }
        return Response(response, status=status.HTTP_201_CREATED)


class UserBookedAppointmentListView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="List of all appointments booked by a user",
        operation_description="List of all appointments booked by a user",
        tags=['Appointment'],
        responses={
            200: UserBookedAppointmentSerializer(many=True),
            404: "Not Found"
        }
    )
    def get(self, request):
        user = request.user
        appointments = Appointment.objects.filter(user=user, status="booked").order_by('-date')
        paginator = BasePagination()
        result_page = paginator.paginate_queryset(appointments, request)
        serializer = UserBookedAppointmentSerializer(result_page, many=True)
        response = {
            "status": "success",
            "message": "User booked appointments retrieved successfully",
            "data": serializer.data
        }
        return paginator.get_paginated_response(response)


class ListUserAllActiveAppointmentView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="List of all active appointments booked by a user",
        operation_description="List of all active appointments booked by a user",
        tags=['Appointment'],
        responses={
            200: UserBookedAppointmentSerializer(many=True),
            404: "Not Found"
        }
    )
    def get(self, request):
        user = request.user
        status = ["booked", "on-waiting", "on-process"]
        appointments = Appointment.objects.filter(user=user, status__in=status).order_by('-date')
        paginator = BasePagination()
        result_page = paginator.paginate_queryset(appointments, request)
        serializer = UserBookedAppointmentSerializer(result_page, many=True)
        response = {
            "status": "success",
            "message": "User booked appointments retrieved successfully",
            "data": serializer.data
        }
        return paginator.get_paginated_response(response)


class ListUserBookedAppointmentHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="List of all history of appointments booked by a user",
        operation_description="List of all history of appointments booked by a user",
        tags=['Appointment'],
        responses={
            200: UserBookedAppointmentSerializer(many=True),
            404: "Not Found"
        }
    )
    def get(self, request):
        user = request.user
        appointments = Appointment.objects.filter(user=user, status="finished").order_by('-date')
        paginator = BasePagination()
        result_page = paginator.paginate_queryset(appointments, request)
        serializer = UserBookedAppointmentSerializer(result_page, many=True)
        response = {
            "status": "success",
            "message": "User booked appointments history retrieved successfully",
            "data": serializer.data
        }
        return paginator.get_paginated_response(response)


class RetrieveUpdateDestroyUserBookedAppointmentView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Retrieve a booked appointment by a user",
        operation_description="Retrieve a booked appointment",
        tags=['Appointment'],
        responses={
            200: UserBookedAppointmentSerializer(),
            404: "Not Found"
        }
    )
    def get(self, request, pk):
        user = request.user
        appointment = get_object_or_404(Appointment, pk=pk, user=user)
        appointment.save()
        serializer = UserBookedAppointmentSerializer(appointment)
        response = {
            "status": "success",
            "message": "User booked appointment retrieved successfully",
            "data": serializer.data
        }
        appointment.save()
        return Response(response, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="Update a booked appointment by a user",
        operation_description="Update a booked appointment",
        tags=['Appointment'],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'notes': openapi.Schema(type=openapi.TYPE_STRING),
                'time': openapi.Schema(type=openapi.TYPE_STRING),
                'date': openapi.Schema(type=openapi.TYPE_STRING),
                'service_provider': openapi.Schema(type=openapi.TYPE_STRING),
                'service': openapi.Schema(type=openapi.TYPE_STRING),
            }
        ),
        responses={
            200: UserBookedAppointmentSerializer(),
            400: "Bad Request"
        }
    )
    def patch(self, request, pk):
        user = request.user
        data = request.data

        # Extract date and time from the request data
        new_date = data.get('date')
        new_time = data.get('time')
        required_fields = all([new_date, new_time])

        # check if the date and time are provided
        if not required_fields:
            response = {
                "status": "error",
                "message": "Date and time are required"
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        # Get the appointment object
        appointment = get_object_or_404(Appointment, pk=pk, user=user)

        

        # Validate date and time format for the new date and/or time
        try:
            if new_date:
                new_date = datetime.strptime(new_date, "%Y-%m-%d").date()
            if new_time:
                new_time = datetime.strptime(new_time, "%H:%M:%S").time()
        except ValueError:
            response = {
                "status": "error",
                "message": "Invalid date or time format"
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if the new date is in the past and if the new time is in the past
        if new_date:
            if new_date < datetime.now().date():
                response = {
                    "status": "error",
                    "message": "Date provided is in the past"
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
        if new_time:
            if new_date == datetime.now().date() and new_time < datetime.now().time():
                response = {
                    "status": "error",
                    "message": "Time provided is in the past"
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if the service provider is available on the given date
        if new_date:
            availability_date = ServiceProviderAvailability.objects.filter(
                date=new_date,
                service_provider=appointment.service_provider,
                start_time__lte=new_time,
                end_time__gte=new_time
            ).first()
        
        if not availability_date:
            response = {
                "status": "error",
                "message": "Service provider is not available at the given date or time"
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        

        # Update the appointment with the new date and/or time
        if new_date:
            appointment.date = new_date
        if new_time:
            appointment.time = new_time

        # Save the updated appointment
        appointment.save()

        # Serialize and return the updated appointment
        serializer = AppointmentSerializer(appointment)
        response = {
            "status": "success",
            "message": "Appointment updated successfully",
            "data": serializer.data
        }
        return Response(response, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="Delete a booked appointment by a user",
        operation_description="Delete a booked appointment",
        tags=['Appointment'],
        responses={
            204: "No Content",
            404: "Not Found"
        }
    )
    def delete(self, request, pk):
        user = request.user
        appointment = get_object_or_404(Appointment, pk=pk, user=user)
        appointment.delete()
        response = {
            "status": "success",
            "message": "User booked appointment deleted successfully",
        }
        return Response(response, status=status.HTTP_204_NO_CONTENT)