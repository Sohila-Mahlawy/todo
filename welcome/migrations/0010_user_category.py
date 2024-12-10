# Generated by Django 4.2.16 on 2024-12-09 22:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('welcome', '0009_project_members'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='category',
            field=models.CharField(choices=[('programming', 'Programming'), ('education', 'Education'), ('crm', 'CRM')], default=None, max_length=20),
        ),
    ]