# Generated by Django 4.2.16 on 2024-12-09 22:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('welcome', '0011_alter_user_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='category',
        ),
    ]
