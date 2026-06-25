import django_filters
from apps.tasks.models import Task


class TaskFilter(django_filters.FilterSet):
    title    = django_filters.CharFilter(lookup_expr='icontains', label='Название содержит')
    status   = django_filters.ChoiceFilter(choices=Task.Status.choices)
    employee = django_filters.NumberFilter(field_name='employee__id', label='ID сотрудника')
    due_from = django_filters.DateFilter(field_name='due_date', lookup_expr='gte', label='Срок с')
    due_to   = django_filters.DateFilter(field_name='due_date', lookup_expr='lte', label='Срок до')

    class Meta:
        model  = Task
        fields = ['title', 'status', 'employee', 'due_from', 'due_to']
