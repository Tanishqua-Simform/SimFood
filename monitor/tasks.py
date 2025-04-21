'''
Monitor/Tasks.py - It contains Asynchronous tasks to be executed outsside the main thread.
1. Fill stats table daily with the data from users model.
2. Clear Monthly Analysis Cache.
3. Clear Daily Analysis Cache.
'''
from datetime import datetime
from celery import shared_task
from django.db import connection
from django.core.cache import cache
from .models import MenuModel

@shared_task
def fill_stats_table():
    ''' Fill the stats table with analysis data, daily @4:30 Pm'''
    # Using Filter and not Get because on holidays we won't have any menu so get will raise error
    menu = MenuModel.objects.filter(date=datetime.now().date())
    if len(menu) > 0:
        with connection.cursor() as cursor:
            result = cursor.execute(f"CALL public.fill_stats_daily('{menu[0].date}')")
            print(result)
    else:
        print("Today it was day-off for Simform Kitchen")

@shared_task
def delete_monthly_analysis_cache():
    ''' Delete Monthly Analysis Cache on 1st of every month'''
    cache.delete('monthly')

@shared_task
def delete_daily_analysis_cache():
    ''' Delete Daily Analysis Cache at midnight everyday'''
    cache.delete('daily')
