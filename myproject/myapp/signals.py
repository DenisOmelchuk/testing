from django.dispatch import receiver
from django.db.models.signals import post_migrate, post_save, pre_save
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import get_template
from .models import CustomUser, EmailConfirmationToken
#
#
# @receiver(post_save, sender=CustomUser)
# def send_confirmation_email(sender, instance, *args, **kwargs):
#     token = EmailConfirmationToken.objects.create(user=instance.id)
#     data = {
#         'user_id': str(instance.id),
#         'token_id': str(token.id),
#     }
#     message = get_template('confirmation_email.txt').render(data)
#     send_mail(subject='Please confirm Email',
#               message=message,
#               from_email=settings.EMAIL_HOST_USER,
#               recipient_list=[instance.email],
#               fail_silently=False)

from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import get_template
from .models import EmailConfirmationToken, CustomUser
from django.apps import apps


@receiver(post_save, sender=CustomUser)
def create_email_confirmation_token(sender, instance, created, **kwargs):
    if created:
        token = EmailConfirmationToken.objects.create(user=instance)
        data = {
            'user_id': str(instance.id),
            'token_id': str(token.id),
        }
        message = get_template('confirmation_email.txt').render(data)
        send_mail(subject='Please confirm Email',
                  message=message,
                  from_email=settings.EMAIL_HOST_USER,
                  recipient_list=[instance.email],
                  fail_silently=False)


def connect_signals(sender, **kwargs):
    if apps.ready:
        post_save.connect(create_email_confirmation_token, sender=CustomUser)




