# Generated by Django 4.2 on 2025-04-11 06:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_alter_simfooduser_role'),
    ]

    operations = [
        migrations.AddField(
            model_name='simfooduser',
            name='paid_next_month',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='simfooduser',
            name='role',
            field=models.CharField(choices=[('cook', 'Cook'), ('headchef', 'Headchef'), ('consumer', 'Consumer'), ('monitor', 'Monitor')], default='Consumer', max_length=8),
        ),
    ]
