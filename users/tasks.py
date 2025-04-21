'''
Users/Tasks.py - It contains Asynchronous tasks to be executed outsside the main thread.
1. Set will_eat to false everyday after lunch.
2. Set Subscription to inactive only for consumers(employees),
3. 
'''
from celery import shared_task
from django.db import connection

@shared_task
def set_will_eat_false():
    ''' Set Will_eat field of SimfoodUser model to False everyday @5 Pm'''
    with connection.cursor() as cursor:
        # result = cursor.callproc('set_simfooduser_will_eat_false')
        result = cursor.execute('CALL public.set_simfooduser_will_eat_false();')
        print(result)

@shared_task
def set_subscription_active_false():
    ''' Set Subscription_active field of SimfoodUser model to False on 
    1st of every month only for those who have not paid for next month.'''
    with connection.cursor() as cursor:
        result = cursor.execute('CALL public.set_simfooduser_subscription_active_false();')
        print(result)
