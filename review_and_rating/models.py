from django.db import models
from accounts.models import CustomUser
from professional_service_provider.models import ServiceProviderProfile
from services.models import Service


class ReviewAndRating(models.Model):
    id = models.BigAutoField(primary_key=True, unique=True, null=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    service_provider = models.ForeignKey(ServiceProviderProfile, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    rating = models.IntegerField(blank=True, null=True)
    review_text = models.TextField(blank=True, null=True)
    review_date = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email} - {self.service_provider.business_name} - {self.service.service_name} - {self.rating} - {self.review_text}"

