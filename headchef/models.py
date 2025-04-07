from django.db import models
from users.models import SimfoodUser
from multiselectfield import MultiSelectField

class TaskModel(models.Model):
    status_choice = (
        ("Pending", "pending"),
        ("Completed", "completed")
    )
    title=models.CharField(max_length=100)
    description=models.TextField()
    status=models.CharField(max_length=9, choices=status_choice, default='pending')
    assigned_by=models.ForeignKey(SimfoodUser, on_delete=models.CASCADE, related_name='assigned_tasks')
    assigned_to=models.ForeignKey(SimfoodUser, on_delete=models.CASCADE, related_name='received_tasks')
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class MenuModel(models.Model):
    DAL_CHOICES = (
        ('Dal Fry', 'dal_fry'),
        ('Gujarati Dal', 'gujarati_dal'),
        ('Mix Dal', 'mix_dal'),
        ('Punjabi Dal', 'punjabi_dal'),
        ('Khatti Meethi Dal', 'khatti_meethi_dal'),
        ('Dal Tadka', 'dal_tadka'),
        ('Kadhi', 'kadhi')
    )
    RICE_CHOICES = (
        ('Plain Rice', 'plain_rice'),
        ('Jeera Rice', 'jeera_rice'),
        ('Pulao', 'pulao'),
        ('Veg Biryani', 'veg_biryani')
    )
    SABZI_CHOICES = (
        ('Aloo Bhindi','aloo_bhindi'),
        ('Butter Paneer','butter_paneer'),
        ('Gobi Aloo','gobi_aloo'),
        ('Tinda','tinda'),
        ('Lasaniya Aloo','lasaniya_aloo'),
        ('Mix Veg','mix_veg'),
        ('Dahi Aloo','dahi_aloo'),
        ('Rajma','rajma'),
        ('Chole','chole'),
        ('Tuver','tuver'),
    )
    ROTI_CHOICES = (
        ('Plain Roti','plain_roti'),
        ('Bajra Roti','bajra_roti'),
        ('Puri','puri'),
        ('Baati','baati'),
        ('Parantha','parantha')
    )
    EXTRA_CHOICES = (
        ('Salad','salad'),
        ('Pickle','pickle'),
        ('Jaggery','jaggery'),
        ('Pappad','Pappad'),
        ('Sandwich Dhokla','sandwich_dhokla'),
        ('Bakharwadi','bakharwadi'),
        ('Fulwadi','fulwadi'),
        ('Patra','patra'),
        ('Bhajiya','bhajiya'),
        ('Khandvi','khandvi'),
        ('Khaman','khaman')
    )
    JAIN_DAL_CHOICES = (
        ('Gujarati Dal', 'gujarati_dal'),
        ('Mix Dal', 'mix_dal'),
        ('Khatti Meethi dal', 'khatti_meethi_dal'),
        ('Kadhi', 'kadhi')
    )
    JAIN_SABZI_CHOICES = (
        ('Pappad nu shak', 'pappad_nu_shak'),
        ('Kela nu shak', 'kela_nu_shak'),
        ('Kobij', 'kobij'),
        ('Rajma', 'rajma'),
        ('Chole', 'chole'),
        ('Tuver', 'tuver')
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
        return self.date
