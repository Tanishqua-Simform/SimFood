from celery import shared_task
from .models import SimfoodUser
from django.db import connection

@shared_task
def set_will_eat_false():
    with connection.cursor() as cursor:
        # result = cursor.callproc('set_simfooduser_will_eat_false')
        result = cursor.execute('CALL public.set_simfooduser_will_eat_false();')
        print(result)

@shared_task
def set_subscription_active_false():
    with connection.cursor() as cursor:
        result = cursor.execute('CALL public.set_simfooduser_subscription_active_false();')
        print(result)

@shared_task
def send_payment_reminder_mail():
    pass
