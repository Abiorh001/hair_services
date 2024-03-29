from django.db import models
from accounts.models import CustomUser
from professional_service_provider.models import (
    ServiceProviderProfile,
    ServiceProviderAvailability,
)
from services.models import Service


class Appointment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    service_provider = models.ForeignKey(ServiceProviderProfile, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=20, choices=[
        ('booked', 'Booked'),
        ('cancelled', 'Cancelled'),
        ('on-waiting', 'On Waiting'),
        ('on-process', 'On Process'),
        ('finished', 'Finished'),
    ], default='booked')
    notes = models.TextField(null=True, blank=True, max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Appointment for {self.service_provider.user.email} on {self.date} at {self.time}"


class AppointmentCheckout(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    payment_status = models.CharField(max_length=50, choices=PAYMENT_STATUS_CHOICES, default='pending')
    payment_method = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Appointment ID: {self.appointment.id} - Payment Status: {self.payment_status}"
        
        

