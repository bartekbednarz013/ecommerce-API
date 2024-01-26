from celery import shared_task
from django.core.mail import send_mail
from .models import Order


@shared_task
def send_payment_reminder(order_id):
    order = Order.objects.get(id=order_id)
    mail_subject = f"Przypomnienie o płatności"
    mail_message = f"Dzień dobry,\nprzypominamy o płatności za zamówienie nr {order.id} z dnia {order.date}.\nKwota do zapłaty: {order.total}zł.\nTermin płatności: {order.payment_date}"
    send_mail(
        subject=mail_subject,
        message=mail_message,
        from_email="ecommerce@example.com",
        recipient_list=[order.client.email],
    )
