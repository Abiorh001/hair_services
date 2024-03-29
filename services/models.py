from django.db import models
from professional_service_provider.models import ServiceProviderProfile
from service_categories.models import ServiceCategory


class Service(models.Model):
    id = models.BigAutoField(primary_key=True, unique=True, null=False)
    service_provider = models.ForeignKey(ServiceProviderProfile, on_delete=models.CASCADE)
    service_category = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE)
    service_name = models.CharField(max_length=255, blank=False, null=False)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    duration_minutes = models.IntegerField(null=False)
    service_picture = models.ImageField(upload_to='service_pictures/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.service_name

