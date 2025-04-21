'''
Headchef/Signals.py - It contains signal for -
1. Deleting cache if Updation or deletion performed on any menu object.
'''
from django.dispatch import receiver
from django.core.cache import cache
from django.db.models.signals import post_delete, post_save
from .models import MenuModel

@receiver([post_save, post_delete], sender=MenuModel)
def delete_menu_cache(sender, **kwargs):
    ''' Delete Menu (key/value) from Redis Cache.'''
    cache.delete('menu')
