# Generated by Django 5.1.2 on 2024-11-21 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('welcome', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='is_notified',
            field=models.BooleanField(default=False),
        ),
    ]
