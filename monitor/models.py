'''
Monitor/Models.py - It contains models for 
1. Stats - To contain the data of people came to eat and chose not to,
on a daily basis for monhtly analysis.
'''
from django.db import models
from headchef.models import MenuModel

class StatsModel(models.Model):
    ''' Model to operate the database Table Stats in Postgres.'''
    menu_id=models.ForeignKey(MenuModel, on_delete=models.CASCADE, related_name="menu_stats")
    chose_yes_came=models.IntegerField()
    chose_yes_not_came=models.IntegerField()
    chose_no=models.IntegerField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.date)
