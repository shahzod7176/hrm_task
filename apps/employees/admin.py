from django.contrib import admin
from .models import Employee


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display  = ('full_name', 'position', 'phone', 'email', 'salary', 'hired_date')
    list_filter   = ('position', 'hired_date')
    search_fields = ('full_name', 'email', 'phone')
    ordering      = ('-created_at',)
