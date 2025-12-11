from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .models import Order


@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=True, max_retries=5)
def send_order_email_task(self, order_id):
    order = Order.objects.select_related('customer', 'customer__user').get(id=order_id)

    # проверка, есть ли email
    if order.customer.user.email:
        subject = f"Order #{order.id} created"
        message = f"Dear {order.customer.first_name}, your order #{order.id} has been received."
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [order.customer.user.email], fail_silently=False)
    else:
        # если email нет — выводим в консоль
        print(f"No email for customer {order.customer}. Order #{order.id} created.")