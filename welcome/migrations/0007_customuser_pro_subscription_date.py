# Generated by Django 5.1.2 on 2024-12-21 19:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('welcome', '0006_prousertask_assigned_to'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='pro_subscription_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
