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
        send_confirmation_email(instance, token)


def send_confirmation_email(user, token):
    data = {
        'user_id': str(user.id),
        'token_id': str(token.id),
    }
    message = get_template('confirmation_email.txt').render(data)
    send_mail(
        subject='Please confirm Email',
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user.email],
        fail_silently=False
    )


def connect_signals(sender, **kwargs):
    if apps.ready:
        post_save.connect(create_email_confirmation_token, sender=CustomUser)

