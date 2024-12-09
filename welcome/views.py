from django.shortcuts import render, redirect,get_object_or_404
from datetime import datetime
from .models import Task,Category,BusinessType,Project,TaskFeedback,CodeSubmission,Invitation,UserRole
from django.http import JsonResponse
import json
import uuid
from .forms import CategoryForm,ProjectForm,InviteMembersForm,UserRegistrationForm,TaskForm
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required
from .models import User,Project,TeamMember
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse
from django.conf import settings




def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        subscription_type = "free"
       

        # Validate form data
        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'register.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return render(request, 'register.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email is already registered.')
            return render(request, 'register.html')

        # Create the user
        user = User.objects.create_user(username=username, email=email, password=password)
        user.subscription_type = subscription_type  # Assuming a profile or extended user model
        user.save()

        # Log the user in after registration
        login(request, user)
        messages.success(request, 'Registration successful!')
        return redirect('list_tasks')

    return render(request, 'register.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {username}!')
            return redirect('list_tasks')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'login.html')

@login_required
def user_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('login')


@login_required
def create_task(request):
    if request.method == 'POST':
        task_name = request.POST.get('title')
        due_time_str = request.POST.get('date')
        category_id = request.POST.get('category')
        project_id = request.POST.get('project')

        # Parse and assign attributes
        due_time = datetime.strptime(due_time_str, '%Y-%m-%dT%H:%M')
        category = get_object_or_404(Category, id=category_id)
        project = get_object_or_404(Project, id=project_id)

        task = Task(
            name=task_name,
            due_date=due_time,
            category=category,
            project=project,
            assigned_to=request.user
        )
        task.save()  # Explicit save call
        return redirect('list_tasks')

    categories = Category.objects.all()
    projects = Project.objects.filter(created_by=request.user)
    return render(request, 'create_task.html', {'categories': categories, 'projects': projects})

def list_tasks(request):
    user = request.user  # Get the logged-in user
    tasks = Task.objects.all()  # Adjust filtering as needed
    categories = Category.objects.all()

    # Check subscription type
    subscription_type = getattr(user, 'subscription_type', 'free')  # Default to 'free' if not set
    if subscription_type == 'free':
        # Free users: Keep the default simple view
        tasks_data = [
            {
                "id": task.id,
                "task_name": task.task_name,
                "due_date": task.due_date.strftime("%H:%M"),
                "is_done": task.is_done
                
            }
            for task in tasks
        ]
        template = "index.html"  # Simple template for free users
        projects = None
    elif subscription_type == 'pro':
        # Pro users: Add programming-specific layout
        tasks_data = [
            {
                "id": task.id,
                "task_name": task.task_name,
                "due_date": task.due_date.strftime("%H:%M"),
                "is_done": task.is_done,
            }
            for task in tasks
        ]
        if user.category == "programming":
            template = "pro_programming_tasks.html"  # Advanced template for pro users
        elif user.category == "crm":
            template = "pro_crm_tasks.html"
        elif user.category == "education":
            template = "pro_education_tasks.html"

        projects = Project.objects.filter(created_by=user)


    return render(request, template, {
        'tasks': tasks_data,
        'categories': categories,
        'projects':projects
    })

def update_task_status(request, task_id):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            is_done = data.get("is_done", False)

            task = get_object_or_404(Task, pk=task_id)
            task.is_done = is_done
            task.save()  # Explicit save
            return JsonResponse({"success": True, "task_id": task.id, "is_done": task.is_done})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=405)

    

def create_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm()

    return render(request, 'create_category.html', {'form': form})


# List Categories
def category_list(request):
    categories = Category.objects.all()  # Get all categories
    return render(request, 'category_list.html', {'categories': categories})


def tasks_by_category(request, category_id):
    # Get the category by ID
    category = get_object_or_404(Category, id=category_id)
    
    # Filter tasks by category
    tasks = Task.objects.filter(category=category).exclude(task_name__exact="")
    
    tasks_data = [
        {
            "id": task.id,
            "task_name": task.task_name,
            "due_time": task.due_time.strftime("%H:%M"),
            "is_done": task.is_done
        }
        for task in tasks
    ]
    
    return render(request, 'tasks_by_category.html', {
        'category': category,
        'tasks': tasks_data
    })




def trial_middleware(get_response):
    def middleware(request):
        if request.user.is_authenticated:
            user_role = getattr(request.user, 'userrole', None)
            if user_role and user_role.trial_start_date:
                trial_end_date = user_role.trial_start_date + timedelta(weeks=2)
                if datetime.now() > trial_end_date:
                    user_role.role = 'expired'  # Mark role as expired
                    user_role.save()  # Save explicitly
                    return redirect('trial_expired')
        return get_response(request)
    return middleware



@login_required
def subscribe_pro(request):
    if request.method == 'POST':
        user = request.user
        category = request.POST.get('category')  # Get the selected category from the form

        # Ensure there is a UserRole instance for the user
        user_role, created = UserRole.objects.get_or_create(user=user)

        # Update the role and business_type fields
        user_role.role = 'team_leader'  # Assign the team leader role
        user_role.business_type = BusinessType.objects.first()  # Set the first available business type (or adjust as needed)
        user_role.save()

        # Update the user's subscription_type and category
        user.subscription_type = 'pro'
        user.category = category  # Save the selected category
        user.save()

        return redirect('list_tasks')  # Redirect to the next step after subscribing

    return render(request, 'subscribe_pro.html', {'user': request.user})



from django.core.mail import send_mail
from django.contrib import messages
from .models import Invitation

@login_required
def invite_team_members(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    # Ensure only the project creator can invite members
    if request.user != project.created_by:
        return redirect('project_detail', project_id=project.id)

    if request.method == 'POST':
        email = request.POST.get("email")

        if email:
            # Create an invitation token
            token = uuid.uuid4()
            Invitation.objects.create(
                email=email,
                project=project,
                team_leader=request.user,
                token=token,
            )

            # Send invitation email
            send_invitation_email(request.user, email, token, request)

            return render(request, 'invitation_sent.html', {'email': email})

    return render(request, 'add_team_members.html', {'project': project})


def send_invitation_email(team_leader, email, token, request):
    # Use reverse to generate the URL for accepting the invitation
    invitation_link = request.build_absolute_uri(reverse('accept_invitation', kwargs={'token': token}))
    send_mail(
        subject="You're Invited to Join a Project!",
        message=f"Hi,\n\nYou've been invited by {team_leader.username} to join the project '{team_leader.username}'.\n\nClick the link below to accept the invitation:\n{invitation_link}\n\nThanks!",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
    )






@login_required
def accept_invitation(request, token):
    invitation = get_object_or_404(Invitation, token=token, is_accepted=False)

    # Add the user to the project
    invitation.project.members.add(request.user)
    invitation.is_accepted = True
    invitation.save()

    return render(request, 'invitation_accepted.html', {'project': invitation.project})




@login_required
def create_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.created_by = request.user  # Set the creator as the logged-in user (team leader)
            project.save()
            return redirect('project_detail', project_id=project.id)  # Redirect to the project detail page
    else:
        form = ProjectForm()

    return render(request, 'create_project.html', {'form': form})


@login_required
def assign_task(request, project_id):
    project = Project.objects.get(id=project_id)

    if request.user != project.created_by:
        return redirect('project_detail', project_id=project.id)  # Only the creator can assign tasks

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.project = project  # Associate the task with the current project
            task.save()
            return redirect('project_detail', project_id=project.id)
    else:
        form = TaskForm()

    return render(request, 'assign_task.html', {'form': form, 'project': project})


@login_required
def project_detail(request, project_id):
    # Fetch the project by ID
    project = get_object_or_404(Project, id=project_id)

    # Ensure the logged-in user is authorized to view the project
    if request.user != project.created_by:
        return render(request, '403.html')  # Unauthorized access page

    # Fetch related tasks and members
    tasks = Task.objects.filter(project=project)
    members = project.members.all()

    # Render the project detail template
    return render(request, 'project_detail.html', {
        'project': project,
        'tasks': tasks,
        'members': members
    })

