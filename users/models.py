'''
Users/Models.py - It contains models for 
1. SimfoodUser (email, first_name, last_name, role, subscription_active, paid_next_month, 
prefer_jain_food, will_eat, came_to_eat, is_active, is_staff) informatin.
2. Custom User Manager for custom user model.
'''
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class CustomUserManager(BaseUserManager):
    ''' Custom user manager to manage the required fields of our custom user model'''
    def create_user(self, email, password, **extra_fields):
        ''' Create SimFood User in model.'''
        if not email or not password:
            raise ValueError('The email and password field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        ''' Create SimFood SuperUser in model.'''
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class SimfoodUser(AbstractBaseUser, PermissionsMixin):
    ''' SimfoodUser with custom fields to manage business required data.'''
    ROLE_CHOICES = {
        ('consumer', 'Consumer'),
        ('cook', 'Cook'),
        ('headchef', 'Headchef'),
        ('monitor', 'Monitor')
    }
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    role = models.CharField(max_length=8, choices=ROLE_CHOICES, default='Consumer')
    subscription_active = models.BooleanField(default=False)
    paid_next_month = models.BooleanField(default=False)
    prefer_jain_food = models.BooleanField(default=False)
    will_eat = models.BooleanField(default=False)
    came_to_eat = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'password']

    def __str__(self):
        return str(self.email)
    