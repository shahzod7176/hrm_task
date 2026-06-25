from django.contrib import admin
from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display  = ('title', 'employee', 'status', 'due_date', 'created_at')
    list_filter   = ('status', 'due_date')
    search_fields = ('title', 'description', 'employee__full_name')
    ordering      = ('-created_at',)
