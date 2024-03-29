from celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_verification_email(email, two_factor_auth_token):
    subject = "Confirm your email"
    message = f"Your two factor authentication token is {two_factor_auth_token}"
    from_email = "hairsolproject@gmail.com"
    recipient = [email]
    send_mail(subject, message, from_email, recipient)
