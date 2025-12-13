from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings

from .models import Customers, EmailVerificationToken


@receiver(post_save, sender=User)
def create_customer_and_verification(sender, instance, created, **kwargs):
    if created:
        # 1. создаём профиль покупателя
        Customers.objects.create(
            user=instance,
            first_name='',
            last_name='',
            age=0
        )

        # 2. деактивируем аккаунт до подтверждения
        instance.is_active = False
        instance.save(update_fields=['is_active'])

        # 3. создаём токен
        token = EmailVerificationToken.objects.create(user=instance)

        # 4. отправляем письмо
        verification_link = f"http://localhost:8000/api/verify-email/{token.token}/"

        send_mail(
            subject="Verify your email",
            message=f"Confirm your email: {verification_link}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[instance.email],
        )
