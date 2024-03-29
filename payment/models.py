from django.db import models
from accounts.models import CustomUser
from appointment_booking.models import Appointment, AppointmentCheckout
from services.models import Service
from professional_service_provider.models import ServiceProviderProfile
from products.models import Product, ProductOrder, ProductCheckout



class ServiceProviderServicesTransaction(models.Model):
    appointment_checkout = models.ForeignKey(AppointmentCheckout, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    service_provider = models.ForeignKey(ServiceProviderProfile, on_delete=models.CASCADE)
    admin_commision = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    service_provider_earning = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.service:
            return f"Service Transaction for {self.service.service_name}"
        else:
            return f"Appointment Transaction for {self.appointment_checkout.appointment.service_provider.user.email}"
    

class ServiceProviderProductsTransaction(models.Model):
    product_order = models.ForeignKey(ProductOrder, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    service_provider = models.ForeignKey(ServiceProviderProfile, on_delete=models.CASCADE)
    admin_commision = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    service_provider_earning = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        if self.product:
            return f"Product Transaction for {self.product.product_name}"
        else:
            return f"Product Transaction for {self.product_order.product.product_name}"


    
