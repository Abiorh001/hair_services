from django.db import models
from django.contrib.auth.models import AbstractUser
from .base_manager import CustomUserManager
from django.utils.translation import gettext_lazy as _
import uuid


class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                               editable=False, unique=True, null=False)
    username = models.CharField(max_length=50, blank=True, null=True, unique=True)

    email = models.EmailField(_('email address'), unique=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True, unique=True)
    referral_code = models.CharField(max_length=50, blank=True, null=True, unique=True)
    two_factor_complete = models.BooleanField(default=False)
    two_factor_auth_token = models.CharField(max_length=6,
                                             blank=True, null=True)
    two_factor_auth_token_expiry = models.DateTimeField(blank=True, null=True)
    reset_password_token = models.CharField(max_length=6,
                                            blank=True, null=True)
    last_login = models.DateTimeField(auto_now=True)
    user_type = models.CharField(max_length=50, blank=True, null=True)
    user_ip_address = models.GenericIPAddressField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class UserProfile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                               editable=False, unique=True, null=False)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    USER_SUBSCRIPTION_CHOICES = [
        ('free', 'Free'),
        ('premium', 'Premium'),
    ]
    user_subscription = models.CharField(max_length=50, choices=USER_SUBSCRIPTION_CHOICES, default='free')
    profile_picture = models.ImageField(upload_to='profile_pictures/',
                                        blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    residential_address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=10)
    country = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.email


class Referral(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                               editable=False, unique=True, null=False)
    referrer_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='referrer')
    referred_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='referred')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
