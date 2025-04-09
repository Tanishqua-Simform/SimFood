from celery import shared_task
from .models import SimfoodUser

@shared_task
def set_will_eat_false():
    queryset = SimfoodUser.objects.all()
    queryset.update(will_eat=False)


@shared_task
def send_payment_reminder_mail():
    pass