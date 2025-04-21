'''
Consumer/Tasks.py - It contains Asynchronous tasks to be executed outsside the main thread.
1. Reminder Email for Payment to consumers.
2. Reminder to set their availability status for subscribed users.
'''
from datetime import date, timedelta
from celery import shared_task
from django.core.mail import send_mail
from users.models import SimfoodUser
from SimFood.settings import EMAIL_HOST_USER

@shared_task
def email_for_payment():
    ''' Email to be sent for payment reminder on 23rd and 28th of every month to 
    consumers(employees)'''
    consumers_not_paid = SimfoodUser.objects.filter(role='consumer', paid_next_month=False)
    next_month = date.today() + timedelta(weeks=2)
    next_month = next_month.strftime('%B')
    title = f'SimFood - Payment due for {next_month}'
    for user in consumers_not_paid:
        msg = f'''Good day {user.first_name.capitalize()},
        \nHope you are doing well.
        \n\nThis mail is to remind you to complete {next_month} month's payment, 
        \nin order to continue enjoying our delicious food.
        \n\nRegards,
        \nSimFood Kitchen.'''
        # send_mail(title, msg, from_email= EMAIL_HOST_USER, recipient_list=[user.email])
        send_mail(
            title,
            msg,
            from_email= EMAIL_HOST_USER,
            recipient_list=['codeblinders5@gmail.com']
            )
    print("Payment Reminder Mail Sent!")

@shared_task
def email_for_set_will_eat_reminder():
    ''' Email to be sent for Availability status updation reminder @8 am to subscribed users.'''
    consumers_not_eating = SimfoodUser.objects.filter(subscription_active=True, will_eat=False)
    today = date.today()
    title = "[Reminder] SimFood - Set your Availaibility for today's lunch."
    for user in consumers_not_eating:
        msg = f'''Good Day {user.first_name.capitalize()},
        \nHope this email finds you well.
        \n\nPlease confirm your availabilty for today ({today}). 
        \nPlease ignore this mail if you won't be joining us today.
        \n\nRegards,
        \nSimFood Kitchen.'''
        # send_mail(title, msg, from_email= EMAIL_HOST_USER, recipient_list=[user.email])
        send_mail(
            title,
            msg,
            from_email= EMAIL_HOST_USER,
            recipient_list=['codeblinders5@gmail.com'])
    print("Set will_eat reminder Mail sent!")
