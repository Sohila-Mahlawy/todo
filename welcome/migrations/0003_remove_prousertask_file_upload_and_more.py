# Generated by Django 5.1.2 on 2024-12-14 21:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('welcome', '0002_loggedusertask_is_done_prousertask_is_done_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='prousertask',
            name='file_upload',
        ),
        migrations.AddField(
            model_name='prousertask',
            name='uploaded_file',
            field=models.FileField(blank=True, null=True, upload_to='task_files/'),
        ),
    ]
