from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework import status
from django.db import connection
from datetime import date
from django.core.cache import cache

@api_view(['GET'])
@permission_classes([AllowAny])
def dashboard(request):
    monthly = cache.get('monthly')
    daily = cache.get('daily')
    # For Past 7 days data
    if not daily:
        print('Cache Miss DAILY')
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM public.stats_analysis_daily()")
            daily = cursor.fetchall()
            cache.set('daily', daily)
    else:
        print('Cache Hit DAILY')
    # For Prev Months Analysis Report
    if not monthly:
        print('Cache Miss MONTHLY')
        with connection.cursor() as cursor:
            today = date.today()
            cursor.execute(f"SELECT * FROM public.stats_analysis_monthly('{today}')")
            monthly = cursor.fetchall()
            cache.set('monthly', monthly)
    else:
        print('Cache Hit MONTHLY')
    day = {}
    if daily:
        for dt, consumers in daily:
            day[str(dt)] = consumers
    else:
        day = 'No data available.'
    if monthly[0][0]:
        month = {
            'consumed': monthly[0][0] * 0.5,
            'wasted': monthly[0][1] * 0.5,
            'saved': monthly[0][2] * 0.5
        }
    else:
        month = 'Previous month data not available.'
    data = {
        'message': 'Data Retrieval Successful',
        'response': {
            'served-people-last-7-days': day,
            'prev-month-food-analysis-in-kgs': month
        }
    }
    return Response(data, status=status.HTTP_200_OK)