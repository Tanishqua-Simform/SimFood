from celery.schedules import crontab

CELERY_BEAT_SCHEDULE = {
    'set_will_eat_to_false': {
        'task': 'users.tasks.set_will_eat_false',
        'schedule': crontab(minute=0, hour=16) # Makes the will_eat attribute of all users to False
    }
}