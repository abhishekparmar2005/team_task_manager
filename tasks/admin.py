from django.contrib import admin
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'project', 'assigned_to', 'status', 'due_date']
    list_filter = ['status', 'project']
    search_fields = ['title']
