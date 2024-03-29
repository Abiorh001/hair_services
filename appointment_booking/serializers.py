from rest_framework import serializers
from .models import Appointment
from accounts.serializers import GetCustomUserSerializer
from services.serializers import ServiceSerializer, GetServiceSerializer
from professional_service_provider.serializers import (
    ServiceProviderProfileSerializer
)


class AppointmentSerializer(serializers.ModelSerializer):
    user = GetCustomUserSerializer(read_only=True)
    service_provider = ServiceProviderProfileSerializer(read_only=True)
    service = ServiceSerializer(read_only=True)

    class Meta:
        model = Appointment
        fields = '__all__'


class UserBookedAppointmentSerializer(serializers.ModelSerializer):
    service = GetServiceSerializer(read_only=True)
    service_provider = ServiceProviderProfileSerializer(read_only=True)
    
    class Meta:
        model = Appointment
        fields = ['id', 'service_provider', 'service', 'status', 'notes', 'date', 'time']


class ServiceProviderBookedAppointmentSerializer(serializers.ModelSerializer):
    service = GetServiceSerializer(read_only=True)
    user = GetCustomUserSerializer(read_only=True)

    class Meta:
        model = Appointment
        fields = ['id', 'user', 'service', 'status', 'notes', 'date', 'time']