from django.db import models
from accounts.models import CustomUser
import uuid
from service_categories.models import ServiceCategory
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import datetime


class ServiceProviderProfile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                               editable=False, unique=True, null=False)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    SERVICE_PROVIDER_SUBSCRIPTION_CHOICES = [
        ('basic', 'Basic'),
        ('premium', 'Premium'),
    ]
    service_provider_subscription = models.CharField(max_length=50, choices=SERVICE_PROVIDER_SUBSCRIPTION_CHOICES, default='basic')
    business_name = models.CharField(max_length=100, unique=True, null=False)
    business_description = models.TextField(blank=True, null=True)
    about_me = models.TextField(blank=True, null=True)
    service_offered = models.ManyToManyField(ServiceCategory, related_name="service_offered")
    profile_picture = models.ImageField(upload_to='profile_pictures/',
                                        blank=True, null=True)
    business_picture = models.ImageField(upload_to='service_provider_shop_pictures/',
                                        blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    business_address = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=10, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.email


class ServiceProviderAvailability(models.Model):
    service_provider = models.ForeignKey(ServiceProviderProfile, on_delete=models.CASCADE)
    date = models.DateField(default=datetime.date.today)
    start_time = models.TimeField(default='00:00:00')
    end_time = models.TimeField(default='23:59:59')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['service_provider', 'date', 'start_time', 'end_time']

    def clean(self):
        # Validate that start_time is before end_time
        if self.start_time >= self.end_time:
            raise ValidationError(_('End time must be after start time.'))

    def __str__(self):
        return f"{self.service_provider.user.email} - {self.date} - {self.start_time} to {self.end_time}"
