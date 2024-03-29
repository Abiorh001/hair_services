# signals.py

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from accounts.models import CustomUser as User
from appointment_booking.models import Appointment
from services.models import Service
from professional_service_provider.models import ServiceProviderProfile
from accounts.models import UserProfile
from products.models import Product, ProductOrder, ProductCheckout
from professional_service_provider.models import ServiceProviderAvailability
from review_and_rating.models import ReviewAndRating
from .models import UserActivity


@receiver(post_save, sender=User)
def user_signup(sender, instance, created, **kwargs):
    print('post_save signal received')
    if created:
        UserActivity.objects.create(
            user=instance,
            activity_type='signup',
            details=f"{instance.first_name} {instance.last_name} signed up."
        )
    print('UserActivity created')


# @receiver(post_save)
# def user_activity(sender, instance, created, **kwargs):
#     print('post_save signal received')
#     if sender != UserActivity and hasattr(instance, 'user'):
#         UserActivity.objects.create(
#             user=instance.user,
#             activity_type='update' if created else 'save',
#             details=f"{instance.__class__.__name__} {instance.id} was saved/updated."
#         )


@receiver(post_save, sender=Appointment)
def appointment_created(sender, instance, created, **kwargs):
    print('post_save signal received')
    if created:
        UserActivity.objects.create(
            user=instance.user,
            activity_type='appointment_created',
            details=f"{instance.user.first_name} {instance.user.last_name} created an appointment. Date of appointment {instance.date} and time {instance.time}."
        )


@receiver(post_save, sender=Service)
def service_created(sender, instance, created, **kwargs):
    print('post_save signal received')
    if created:
        UserActivity.objects.create(
            user=instance.service_provider.user,
            activity_type='service_created',
            details=f"{instance.service_provider.user.first_name} {instance.service_provider.user.last_name} created a new service. Name of Service is {instance.service_name}."
        )


@receiver(post_save, sender=ServiceProviderProfile)
def service_provider_created(sender, instance, created, **kwargs):
    if created:
        UserActivity.objects.create(
            user=instance.user,
            activity_type='service_provider_created',
            details=f"{instance.user.first_name} {instance.user.last_name} created a new professional profile."
        )


@receiver(post_save, sender=UserProfile)
def user_profile_created(sender, instance, created, **kwargs):
    if created:
        UserActivity.objects.create(
            user=instance.user,
            activity_type='user_profile_created',
            details=f"{instance.user.first_name} {instance.user.last_name} created a new user profile."
        )


@receiver(post_save, sender=Product)
def product_created(sender, instance, created, **kwargs):
    if created:
        service_provider = instance.owner
        UserActivity.objects.create(
            user=service_provider.user,
            activity_type='product_created',
            details=f"{instance.owner.business_name} created a new product. Product name is {instance.product_name}."
        )


@receiver(post_save, sender=ProductOrder)
def product_order_created(sender, instance, created, **kwargs):
    if created:
        UserActivity.objects.create(
            user=instance.user,
            activity_type='product_order_created',
            details=f"{instance.user.first_name} {instance.user.last_name} created a new product order. Product name is {instance.product.product_name}."
        )


@receiver(post_save, sender=ProductCheckout)
def product_checkout_created(sender, instance, created, **kwargs):
    if created:
        product = instance.product_order.product
        user = instance.product_order.user
        UserActivity.objects.create(
            user=user,
            activity_type='product_checkout_created',
            details=f"{user.first_name} {user.last_name} created a new product checkout. Product name is {product.product_name}."
        )


@receiver(post_save, sender=ServiceProviderAvailability)
def service_provider_availability_created(sender, instance, created, **kwargs):
    if created:
        UserActivity.objects.create(
            user=instance.service_provider.user,
            activity_type='service_provider_availability_created',
            details=f"{instance.service_provider.user.first_name} {instance.service_provider.user.last_name} created a new schedule availability."
        )


# @receiver(post_save, sender=ReviewAndRating)
# def review_and_rating_created(sender, instance, created, **kwargs):
#     if created:
#         UserActivity.objects.create(
#             user=instance.user,
#             activity_type='review_and_rating_created',
#             details=f"{instance.user.first_name} {instance.user.last_name} created a new review and rating. Rating is {instance.rating}."
#         )
