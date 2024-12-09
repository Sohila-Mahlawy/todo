

from django.urls import path
from . import views

urlpatterns = [
    # Task-related URLs
    path('', views.list_tasks, name='list_tasks'),
    path('create-task/', views.create_task, name='create_task'),
    path('update_task_status/<int:task_id>/', views.update_task_status, name='update_task_status'),
    path('tasks/category/<int:category_id>/', views.tasks_by_category, name='tasks_by_category'),


    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.user_logout, name='logout'),

    path('create_project/', views.create_project, name='create_project'),
    path('project/<int:project_id>/invite/', views.invite_team_members, name='invite_team_members'),
    path('invitation/<uuid:token>/accept/', views.accept_invitation, name='accept_invitation'),
    path('project/<int:project_id>/assign_task/', views.assign_task, name='assign_task'),
    path('project/<int:project_id>/', views.project_detail, name='project_detail'),

    # Category-related URLs
    path('create-category/', views.create_category, name='create_category'),
    path('category-list/', views.category_list, name='category_list'),

    # Subscription-related URLs
    path('subscribe/pro/', views.subscribe_pro, name='subscribe_pro'),
    
    # Team Management URLs
]
