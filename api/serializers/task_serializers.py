from rest_framework import serializers
from apps.tasks.models import Task
from api.serializers.employee_serializers import EmployeeListSerializer


class TaskSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model  = Task
        fields = (
            'id', 'title', 'description',
            'employee', 'status', 'status_display',
            'due_date', 'created_at', 'updated_at',
        )
        read_only_fields = ('created_at', 'updated_at', 'status_display')


class TaskDetailSerializer(serializers.ModelSerializer):
    employee    = EmployeeListSerializer(read_only=True)
    employee_id = serializers.PrimaryKeyRelatedField(
        source='employee',
        queryset=__import__('apps.employees.models', fromlist=['Employee']).Employee.objects.all(),
        write_only=True,
        required=False,
        allow_null=True,
        help_text='ID сотрудника',
    )
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model  = Task
        fields = (
            'id', 'title', 'description',
            'employee', 'employee_id',
            'status', 'status_display',
            'due_date', 'created_at', 'updated_at',
        )
        read_only_fields = ('created_at', 'updated_at', 'status_display')


class ChangeStatusSerializer(serializers.Serializer):
    status = serializers.ChoiceField(
        choices=Task.Status.choices,
        help_text='Новый статус: created | in_progress | done',
    )
