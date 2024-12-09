from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
import uuid
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    # Add custom fields
    subscription_type = models.CharField(
        max_length=10,
        choices=[('free', 'Free'), ('pro', 'Pro')],
        default='free'
    )

    category = models.CharField(
        max_length=20,
        choices=[('programming', 'Programming'), ('education', 'Education'), ('crm', 'CRM')],
        null = True
    )


class BusinessType(models.Model):
    name = models.CharField(max_length=100)

class UserRole(models.Model):
    ROLE_CHOICES = [('team_leader', 'Team Leader'), ('product_owner', 'Product Owner'), ('programmer', 'Programmer')]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)
    business_type = models.ForeignKey(BusinessType, on_delete=models.SET_NULL, null=True)
    trial_start_date = models.DateTimeField(auto_now_add=True)

class Project(models.Model):
    name = models.CharField(max_length=255)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_projects')
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True, blank=True)
    members = models.ManyToManyField(User, related_name='projects', blank=True)


    def __str__(self):
        return self.name


class TeamMember(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='team_members')
    is_invited = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.user.username} - {self.project.name}'

    
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

class Task(models.Model):
    task_name = models.CharField(max_length=255)
    description = models.TextField()
    due_date = models.DateTimeField(null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    is_done = models.BooleanField(default=False)

    def __str__(self):
        return self.task_name

class TaskFeedback(models.Model):
    task = models.OneToOneField(Task, on_delete=models.CASCADE)
    feedback = models.TextField()
    approved = models.BooleanField(default=False)

class CodeSubmission(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='submissions')
    code_file = models.FileField(upload_to='submissions/')
    submitted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    submitted_at = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(null=True)



class Invitation(models.Model):
    team_leader = models.ForeignKey(User, on_delete=models.CASCADE, related_name='invitations')
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    created_at = models.DateTimeField(default=now)
    accepted = models.BooleanField(default=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True)  # Ensure project is linked to the Project model

    def is_valid(self):
        # Example of adding an expiration time (optional)
        return not self.accepted