from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from django.core.mail import send_mail
from django.conf import settings
from .models import EmailVerificationToken
from django.contrib.auth.models import User


@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=True, max_retries=5)
def send_verification_email_task(self, user_id):
    try:
        user = User.objects.get(id=user_id)
        token = user.email_verification.token
    except (User.DoesNotExist, EmailVerificationToken.DoesNotExist):
        print(f"[EMAIL SKIPPED] User id {user_id} or token not found")
        return

    if not user.email:
        print(f"[EMAIL SKIPPED] User {user.username} has no email")
        return

    link = f"{settings.FRONTEND_URL}/verify-email/{token}"
    send_mail(
        subject="Verify your email",
        message=f"Confirm your email: {link}",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
    )


@shared_task
def remind_unverified_users():
    one_day_ago = timezone.now() - timedelta(days=1)
    tokens = EmailVerificationToken.objects.filter(
        user__is_active=False,
        created_at__lte=one_day_ago
    )

    for token in tokens:
        if token.user.email:
            send_mail(
                "Reminder: verify your email",
                f"Verify your email: http://localhost:8000/api/verify-email/{token.token}/",
                settings.DEFAULT_FROM_EMAIL,
                [token.user.email],
            )
        else:
            print(f"[REMINDER SKIPPED] User {token.user.username} has no email")


@shared_task
def deactivate_unverified_users():
    two_days_ago = timezone.now() - timedelta(days=2)
    tokens = EmailVerificationToken.objects.filter(
        user__is_active=False,
        created_at__lte=two_days_ago
    )

    for token in tokens:
        token.user.is_active = False
        token.user.save(update_fields=['is_active'])
