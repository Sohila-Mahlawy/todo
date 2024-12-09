# Generated by Django 5.1.2 on 2024-12-09 07:09

import django.db.models.deletion
import django.utils.timezone
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('welcome', '0004_category_task_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='BusinessType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('start_date', models.DateTimeField(auto_now_add=True)),
                ('end_date', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=150, unique=True)),
                ('subscription_type', models.CharField(choices=[('free', 'Free'), ('pro', 'Pro')], default='free', max_length=10)),
            ],
        ),
        migrations.RenameField(
            model_name='task',
            old_name='is_done',
            new_name='is_completed',
        ),
        migrations.RenameField(
            model_name='task',
            old_name='task_name',
            new_name='name',
        ),
        migrations.RemoveField(
            model_name='task',
            name='category',
        ),
        migrations.RemoveField(
            model_name='task',
            name='due_time',
        ),
        migrations.AddField(
            model_name='task',
            name='due_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='task',
            name='project',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='welcome.project'),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='TaskFeedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feedback', models.TextField()),
                ('approved', models.BooleanField(default=False)),
                ('task', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='welcome.task')),
            ],
        ),
        migrations.AddField(
            model_name='project',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_projects', to='welcome.user'),
        ),
        migrations.CreateModel(
            name='Invitation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('token', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('accepted', models.BooleanField(default=False)),
                ('team_leader', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invitations', to='welcome.user')),
            ],
        ),
        migrations.CreateModel(
            name='CodeSubmission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code_file', models.FileField(upload_to='submissions/')),
                ('submitted_at', models.DateTimeField(auto_now_add=True)),
                ('approved', models.BooleanField(null=True)),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='submissions', to='welcome.task')),
                ('submitted_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='welcome.user')),
            ],
        ),
        migrations.AddField(
            model_name='task',
            name='assigned_to',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tasks', to='welcome.user'),
        ),
        migrations.CreateModel(
            name='UserRole',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(choices=[('team_leader', 'Team Leader'), ('product_owner', 'Product Owner'), ('programmer', 'Programmer')], max_length=50)),
                ('trial_start_date', models.DateTimeField(auto_now_add=True)),
                ('business_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='welcome.businesstype')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='welcome.user')),
            ],
        ),
    ]
