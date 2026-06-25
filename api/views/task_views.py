from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter, OpenApiResponse
from drf_spectacular.types import OpenApiTypes
from apps.tasks.models import Task
from api.serializers.task_serializers import TaskSerializer, TaskDetailSerializer, ChangeStatusSerializer
from api.filters.task_filters import TaskFilter


@extend_schema_view(
    list=extend_schema(
        tags=['tasks'],
        summary='Список задач',
        parameters=[
            OpenApiParameter('status',   OpenApiTypes.STR,  description='created | in_progress | done'),
            OpenApiParameter('employee', OpenApiTypes.INT,  description='ID сотрудника'),
            OpenApiParameter('due_from', OpenApiTypes.DATE, description='Срок с (YYYY-MM-DD)'),
            OpenApiParameter('due_to',   OpenApiTypes.DATE, description='Срок до (YYYY-MM-DD)'),
            OpenApiParameter('search',   OpenApiTypes.STR,  description='Поиск по названию и описанию'),
        ],
    ),
    create=extend_schema(
        tags=['tasks'],
        summary='Создать задачу',
    ),
    retrieve=extend_schema(
        tags=['tasks'],
        summary='Детали задачи',
    ),
    update=extend_schema(
        tags=['tasks'],
        summary='Обновить задачу (полное)',
    ),
    partial_update=extend_schema(
        tags=['tasks'],
        summary='Обновить задачу (частичное)',
    ),
    destroy=extend_schema(
        tags=['tasks'],
        summary='Удалить задачу',
    ),
)
class TaskViewSet(viewsets.ModelViewSet):
    queryset           = Task.objects.select_related('employee').all()
    permission_classes = (permissions.IsAuthenticated,)
    filterset_class    = TaskFilter
    search_fields      = ('title', 'description')
    ordering_fields    = ('created_at', 'due_date', 'status')
    ordering           = ('-created_at',)

    def get_serializer_class(self):
        if self.action in ('retrieve', 'create', 'update', 'partial_update'):
            return TaskDetailSerializer
        return TaskSerializer

    @extend_schema(
        tags=['tasks'],
        summary='Изменить статус задачи',
        request=ChangeStatusSerializer,
        responses={200: TaskSerializer},
    )
    @action(detail=True, methods=['patch'], url_path='change_status')
    def change_status(self, request, pk=None):
        task       = self.get_object()
        serializer = ChangeStatusSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        task.status = serializer.validated_data['status']
        task.save(update_fields=['status', 'updated_at'])
        return Response(TaskSerializer(task).data)

    @extend_schema(
        tags=['tasks'],
        summary='Задачи по сотруднику',
        parameters=[OpenApiParameter('emp_id', OpenApiTypes.INT, location='path', description='ID сотрудника')],
        responses={200: TaskSerializer(many=True)},
    )
    @action(detail=False, methods=['get'], url_path=r'by_employee/(?P<emp_id>\d+)')
    def by_employee(self, request, emp_id=None):
        tasks = self.get_queryset().filter(employee_id=emp_id)
        page  = self.paginate_queryset(tasks)
        if page is not None:
            return self.get_paginated_response(TaskSerializer(page, many=True).data)
        return Response(TaskSerializer(tasks, many=True).data)


