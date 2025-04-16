from celery import shared_task
from users.models import SimfoodUser
from django.core.mail import send_mail
from datetime import date, timedelta
from SimFood.settings import EMAIL_HOST_USER

@shared_task
def email_for_payment():
    consumers_not_paid = SimfoodUser.objects.filter(role='consumer', paid_next_month=False)
    next_month = date.today() + timedelta(weeks=2)
    next_month = next_month.month
    title = f'SimFood - Payment due for {next_month}'
    for user in consumers_not_paid:
        msg = f"Good day {user}, \nHope you are doing well.\n\nThis mail is to remind you to complete {next_month} month's payment, \nin order to continue enjoying our delicious food.\n\nRegards,\nSimFood Kitchen."
        # send_mail(title, msg, from_email= EMAIL_HOST_USER, recipient_list=[user.email])
        send_mail(title, msg, from_email= EMAIL_HOST_USER, recipient_list=['codeblinders5@gmail.com'])
    print("Payment Reminder Mail Sent!")


@shared_task
def email_for_set_will_eat_reminder():
    consumers_not_eating = SimfoodUser.objects.filter(subscription_active=True, will_eat=False)
    today = date.today()
    title = f"[Reminder] SimFood - Set your Availaibility for today's lunch."
    for user in consumers_not_eating:
        msg = f"Good Day {user},\nHope this email finds you well.\n\nPlease confirm your availabilty for {today}. \nPlease ignore this mail if you won't be joining us today.\n\nRegards,\nSimFood Kitchen."
        # send_mail(title, msg, from_email= EMAIL_HOST_USER, recipient_list=[user.email])
        send_mail(title, msg, from_email= EMAIL_HOST_USER, recipient_list=['codeblinders5@gmail.com'])
    print("Set will_eat reminder Mail sent!")