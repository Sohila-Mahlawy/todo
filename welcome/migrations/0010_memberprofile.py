# Generated by Django 5.1.2 on 2024-12-26 18:11

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('welcome', '0009_invitation_role'),
    ]

    operations = [
        migrations.CreateModel(
            name='MemberProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_description', models.TextField()),
                ('role', models.CharField(choices=[('team_leader', 'Team Leader'), ('product_owner', 'Product Owner'), ('programmer', 'Programmer')], max_length=20)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
