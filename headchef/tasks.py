from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from .models import MenuModel
from users.models import SimfoodUser
from datetime import date, timedelta

@shared_task
def email_for_menu():
    active_users = SimfoodUser.objects.filter(subscription_active=True)
    tomorrow = date.today() + timedelta(days=1)
    menu = MenuModel.objects.filter(date=tomorrow).values().first()

    if menu:
        # We made custom filter for this in DTL but using this logic in Jinja instead
        for key in menu:
            val = menu[key]
            if key in ['dal', 'rice', 'sabzi', 'roti', 'jain_sabzi', 'jain_dal']:
                menu[key] = ' '.join([i.capitalize() for i in val.split('_')])
            elif key == 'extras':
                menu[key] = [extras.capitalize() for extras in val]
            elif key == 'date':
                menu[key] = date.strftime(val, '%B %d, %Y')
        
        for user in active_users:
            context = {
                'username': user.first_name,
                'menu': menu
            }
            text_content = render_to_string('menu.txt', context)
            html_content = render_to_string('menu.html', context)
            # mail = EmailMultiAlternatives(f'SimFood - Delicious Meal for {menu["date"]}', text_content, to=[user.email])
            mail = EmailMultiAlternatives(f'SimFood - Delicious Meal for {menu["date"]}', text_content, to=['codeblinders5@gmail.com'])
            mail.attach_alternative(html_content, 'text/html')
            # mail.send(fail_silently=True)
            mail.send()
        print("Menu Mail Sent!")
    else:
        print("No Menu set for tomorrow! So Mail not sent!")