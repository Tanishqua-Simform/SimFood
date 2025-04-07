from django.db import models
from headchef.models import MenuModel

class StatsModel(models.Model):
    menu_id=models.ForeignKey(MenuModel, on_delete=models.CASCADE, related_name="menu_stats")
    chose_yes_came=models.IntegerField()
    chose_yes_not_came=models.IntegerField()
    chose_no=models.IntegerField()

    def __str__(self):
        return self.menu_id