"""
Django settings for SimFood project.

Generated by 'django-admin startproject' using Django 5.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
from datetime import timedelta

import os
from dotenv import load_dotenv

from celery.schedules import crontab

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-4!^k2o2%e@52cp-0z2261bq#gdy5&q-9wiq%558)_r(j+@*$96'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt',
    'django_celery_results',
    'django_celery_beat',
    'bootstrap5',
    'users',
    'headchef',
    'cook',
    'consumer',
    'monitor',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'users.middleware.log_requests.RequestLoggingMiddleware',
]

ROOT_URLCONF = 'SimFood.urls'

TEMPLATES = [
        {
        'BACKEND': 'django.template.backends.jinja2.Jinja2',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
		    # 'environment': 'SimFood.jinja2.environment'
	    }
    },
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    }
]

WSGI_APPLICATION = 'SimFood.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
       'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'simfood',
        'USER': os.getenv('DATABASE_POSTGRES_USER'),
        'PASSWORD': os.getenv('DATABASE_POSTGRES_PASSWORD'),
        'HOST': 'localhost',
        'PORT': ''
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# My Custom User Model
AUTH_USER_MODEL = 'users.SimfoodUser'

# Rest Framework OCnfiguration
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    # Throttling Requests for our Application.
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.ScopedRateThrottle',
        'rest_framework.throttling.AnonRateThrottle',
        # 'rest_framework.throttling.UserRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        # 'user': '50/hr'
        'anon': '100/day',
        'user-get': '10/hr',
        'user-put': '20/day',
        'payment-put': '3/day',
        'user-post': '20/day'
    }
}

# JWT Authentication Configuration
SIMPLE_JWT = {
    # 'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15),
    # 'REFRESH_TOKEN_LIFETIME': timedelta(days=1)

    # While DEVELOPMENT is going on -
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1)
}

# Celery Configuration
### DEPRECATED VARIABLES
# CELERY_BROKER_URL = 'redis://127.0.0.1:6379'
# CELERY_ACCEPT_CONTENT = ['application/json']
# CELERY_RESULT_SERIALIZER = 'json'
# CELERY_TASK_SERIALIZER = 'json'
# # CELERY_RESULT_BACKEND = f'db+postgresql://{os.getenv("DATABASE_POSTGRES_USER")}:{os.getenv("DATABASE_POSTGRES_PASSWORD")}@localhost/simfood'
# CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379'
# CELERY_TIMEZONE = 'Asia/Kolkata'

CELERY_BROKER_URL = 'redis://127.0.0.1:6379'
accept_content = ['application/json']
result_serializer = 'json'
task_serializer = 'json'
# result_backend = f'db+postgresql://{os.getenv("DATABASE_POSTGRES_USER")}:{os.getenv("DATABASE_POSTGRES_PASSWORD")}@localhost/simfood'
result_backend = 'redis://127.0.0.1:6379'
timezone = 'Asia/Kolkata'

# Celery Beat
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'
CELERY_BEAT_SCHEDULE = {
    'daily_email_for_set_will_eat_reminder': {
        'task': 'consumer.tasks.email_for_set_will_eat_reminder',
        'schedule': crontab(minute=0, hour=8) # Sends Will_Eat Reminder Mail Everyday @8 AM to those who have not set this field yet.
    },

    'daily_fill_stats_table': {
        'task': 'monitor.tasks.fill_stats_table',
        'schedule': crontab(minute=30, hour=16) # Fill the Stats table everyday @ 4:30 PM IST.
    },

    'daily_set_will_eat_to_false': {
        'task': 'users.tasks.set_will_eat_false',
        'schedule': crontab(minute=0, hour=17) # Makes the will_eat attribute of all users to False @ 5 PM IST.
    },

    'daily_email_for_menu': {
        'task': 'headchef.tasks.email_for_menu',
        'schedule': crontab(minute=0, hour=18) # Sends Menu for next day from Mail everyday @6 PM to those will active subscription.
    },

    'daily_delete_bar_graph_analysis_cache': {
        'task': 'monitor.tasks.delete_daily_analysis_cache',
        'schedule': crontab(minute=0, hour=0) # Deletes the cache for Daily Stats Data everyday @midnight
    },

    'monthly_set_subscription_active_to_false': {
        'task': 'users.tasks.set_subscription_active_false',
        'schedule': crontab(minute=0, hour=0, day_of_month=1) # Makes the subscription_active attribute of all users to False @12 AM IST on 1st of every month.
    },

    'monthly_email_for_payment': {
        'task': 'consumer.tasks.email_for_payment',
        'schedule': crontab(minute=0, hour=9, day_of_month='23,28') # Sends Payment Reminder Mail on 23rd and 28th of every month @9 AM IST, to those eho have not paid yet.
    },

    'monthly_delete_pie_chart_analysis_cache': {
        'task': 'monitor.tasks.delete_monthly_analysis_cache',
        'schedule': crontab(minute=0, hour=0, day_of_month=1)  # Deletes the cache for Monthly Stats Data on 1st of every month @midnight
    }
}

# Email Configurations
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')

# Redis Configurations
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}
