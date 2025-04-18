from django.dispatch import receiver
from django.core.cache import cache
from django.db.models.signals import post_delete, post_save
from .models import MenuModel

@receiver([post_save, post_delete], sender=MenuModel)
def delete_menu_cache(sender, **kwargs):
    cache.delete('menu')
