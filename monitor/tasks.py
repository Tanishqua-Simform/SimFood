from celery import shared_task
from django.db import connection
from datetime import datetime
from .models import StatsModel
from .models import MenuModel

@shared_task
def fill_stats_table():
    # Using Filter and not Get because on holidays we won't have any menu so get will raise error
    menu = MenuModel.objects.filter(date=datetime.now().date())
    if len(menu) > 0:
        with connection.cursor() as cursor:
            result = cursor.execute(f"CALL public.fill_stats_daily('{menu[0].date}')")
            print(result)
    else:
        print("Today it was day-off for Simform Kitchen")