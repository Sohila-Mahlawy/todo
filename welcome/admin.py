from django.contrib import admin
from .models import Task, Category, BusinessType, Project, TaskFeedback, CodeSubmission, Invitation, UserRole
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('subscription_type', 'category')}),  # Add 'category' field here
    )
    # You can also modify the 'list_display' if you want the 'category' to be shown in the list view of users.
    list_display = UserAdmin.list_display + ('subscription_type', 'category')

admin.site.register(Task)
admin.site.register(Category)
admin.site.register(BusinessType)
admin.site.register(Project)
admin.site.register(TaskFeedback)
admin.site.register(CodeSubmission)
admin.site.register(Invitation)
admin.site.register(UserRole)
