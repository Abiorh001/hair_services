from celery import shared_task
from django.core.mail import send_mail


@shared_task
def resend_two_factor_auth_token(email, token):
    # Your logic to resend the token, for example using Django's send_mail
    subject = 'Two Factor Auth Token'
    message = f'Your new token: {token}'
    from_email = 'hairsolproject@gmail.com'
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list)
