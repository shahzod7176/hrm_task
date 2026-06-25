import django_filters
from apps.employees.models import Employee


class EmployeeFilter(django_filters.FilterSet):
    full_name   = django_filters.CharFilter(lookup_expr='icontains', label='ФИО содержит')
    position    = django_filters.CharFilter(lookup_expr='icontains', label='Должность содержит')
    salary_min  = django_filters.NumberFilter(field_name='salary', lookup_expr='gte', label='Зарплата от')
    salary_max  = django_filters.NumberFilter(field_name='salary', lookup_expr='lte', label='Зарплата до')
    hired_from  = django_filters.DateFilter(field_name='hired_date', lookup_expr='gte', label='Принят с')
    hired_to    = django_filters.DateFilter(field_name='hired_date', lookup_expr='lte', label='Принят до')

    class Meta:
        model  = Employee
        fields = ['full_name', 'position', 'salary_min', 'salary_max', 'hired_from', 'hired_to']
