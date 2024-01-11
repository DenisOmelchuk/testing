from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import get_template


def send_confirmation_email(email, token_id, user_id):
    data = {
        'user_id': str(user_id),
        'token_id': str(token_id),
    }
    message = get_template('myproject/templates/confirmation_email.txt').render(data)
    send_mail(subject='Please confirm Email',
              message=message,
              from_email=settings.EMAIL_HOST_USER,
              recipient_list=[email],
              fail_silently=False)