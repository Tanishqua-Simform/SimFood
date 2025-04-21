'''
Headchef/Models.py - It contains models for 
1. Task Creation (title, description, status, assignedd_by, assigned_to) informatin.
2. Menu Creation (date, dal, rice, sabzi, roti, jian_dal, jain_sabzi, created_by)
'''
from django.db import models
from multiselectfield import MultiSelectField
from users.models import SimfoodUser

class TaskModel(models.Model):
    ''' Model to operate the database Table Tasks in Postgres.'''
    status_choice = (
        ('pending', 'Pending'),
        ('completed', 'Completed')
    )
    title=models.CharField(max_length=100)
    description=models.TextField()
    status=models.CharField(max_length=9, choices=status_choice, default='pending')
    assigned_by=models.ForeignKey(SimfoodUser, on_delete=models.CASCADE, related_name='assigned_tasks')
    assigned_to=models.ForeignKey(SimfoodUser, on_delete=models.CASCADE, related_name='received_tasks')
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.title)

class MenuModel(models.Model):
    ''' Model to operate the database Table Menu in Postgres.'''
    DAL_CHOICES = (
        ('dal_fry', 'Dal Fry'),
        ('gujarati_dal', 'Gujarati Dal'),
        ('mix_dal', 'Mix Dal'),
        ('punjabi_dal', 'Punjabi Dal'),
        ('khatti_meethi_dal', 'Khatti Meethi Dal'),
        ('dal_tadka', 'Dal Tadka'),
        ('kadhi', 'Kadhi')
    )
    RICE_CHOICES = (
        ('plain_rice', 'Plain Rice'),
        ('jeera_rice', 'Jeera Rice'),
        ('pulao', 'Pulao'),
        ('veg_biryani', 'Veg Biryani')
    )
    SABZI_CHOICES = (
        ('aloo_bhindi', 'Aloo Bhindi'),
        ('butter_paneer', 'Butter Paneer'),
        ('gobi_aloo', 'Gobi Aloo'),
        ('tinda', 'Tinda'),
        ('lasaniya_aloo', 'Lasaniya Aloo'),
        ('mix_veg', 'Mix Veg'),
        ('dahi_aloo', 'Dahi Aloo'),
        ('rajma', 'Rajma'),
        ('chole', 'Chole'),
        ('tuver', 'Tuver')
    )
    ROTI_CHOICES = (
        ('plain_roti', 'Plain Roti'),
        ('bajra_roti', 'Bajra Roti'),
        ('puri', 'Puri'),
        ('baati', 'Baati'),
        ('parantha', 'Parantha')
    )
    EXTRA_CHOICES = (
        ('salad', 'Salad'),
        ('pickle', 'Pickle'),
        ('jaggery', 'Jaggery'),
        ('pappad', 'Pappad'),
        ('sandwich_dhokla', 'Sandwich Dhokla'),
        ('bakharwadi', 'Bakharwadi'),
        ('fulwadi', 'Fulwadi'),
        ('patra', 'Patra'),
        ('bhajiya', 'Bhajiya'),
        ('khandvi', 'Khandvi'),
        ('khaman', 'Khaman'),
        ('dhokla', 'Dhokla')
    )
    JAIN_DAL_CHOICES = (
        ('gujarati_dal', 'Gujarati Dal'),
        ('mix_dal', 'Mix Dal'),
        ('khatti_meethi_dal', 'Khatti Meethi Dal'),
        ('kadhi', 'Kadhi')
    )
    JAIN_SABZI_CHOICES = (
        ('pappad_nu_shak', 'Pappad nu shak'),
        ('kela_nu_shak', 'Kela nu shak'),
        ('kobij', 'Kobij'),
        ('rajma', 'Rajma'),
        ('chole', 'Chole'),
        ('tuver', 'Tuver')
    )
    date=models.DateField(unique=True)
    dal=models.CharField(max_length=20, choices=DAL_CHOICES)
    rice=models.CharField(max_length=20, choices=RICE_CHOICES)
    sabzi=models.CharField(max_length=20, choices=SABZI_CHOICES)
    roti=models.CharField(max_length=20, choices=ROTI_CHOICES)
    extras=MultiSelectField(choices=EXTRA_CHOICES, max_choices=5, max_length=50)
    jain_dal=models.CharField(max_length=20, choices=JAIN_DAL_CHOICES)
    jain_sabzi=models.CharField(max_length=20, choices=JAIN_SABZI_CHOICES)
    created_by=models.ForeignKey(SimfoodUser, on_delete=models.CASCADE, related_name="menu_prepared")
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.date)
