# Generated by Django 5.1.2 on 2024-11-21 11:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('welcome', '0002_task_is_notified'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='is_notified',
        ),
    ]