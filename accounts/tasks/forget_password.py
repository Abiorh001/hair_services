from celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_forget_password_email(email, reset_token):
    subject = "Reset your password"
    message = f"Your reset password token is {reset_token}"
    from_email = "hairsolproject@gmail.com"
    recipient = [email]
    send_mail(subject, message, from_email, recipient)