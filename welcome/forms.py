from django import forms
from .models import Category,Project,Task

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']


from django.contrib.auth.forms import UserCreationForm
from .models import User

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'subscription_type']



class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'end_date']  # Add other fields as needed
        widgets = {
            'end_date': forms.DateInput(attrs={'type': 'date'})  # Ensure it appears as a date picker
        }

class InviteMembersForm(forms.Form):
    email = forms.EmailField()




class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['task_name', 'description', 'due_date', 'assigned_to']  # Add other fields as needed
    due_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'})  # This will render the field as a date picker
    )