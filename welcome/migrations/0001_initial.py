# Generated by Django 5.1.2 on 2024-11-21 11:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_name', models.CharField(max_length=255)),
                ('due_time', models.TimeField()),
                ('is_done', models.BooleanField(default=False)),
            ],
        ),
    ]
