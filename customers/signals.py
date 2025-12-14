from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Customers, EmailVerificationToken


@receiver(post_save, sender=User)
def create_customer_and_verification(sender, instance, created, **kwargs):
    if not created:
        return

    Customers.objects.create(
        user=instance,
        first_name=instance.first_name or '',
        last_name=instance.last_name or '',
        age=0
    )

    instance.is_active = False
    instance.save(update_fields=['is_active'])

    EmailVerificationToken.objects.create(user=instance)
