from rest_framework import viewsets, permissions
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

from apps.employees.models import Employee
from api.serializers.employee_serializers import EmployeeSerializer, EmployeeListSerializer
from api.filters.employee_filters import EmployeeFilter


@extend_schema_view(
    list=extend_schema(
        tags=['employees'],
        summary='Список сотрудников',
        parameters=[
            OpenApiParameter('full_name',  OpenApiTypes.STR,  description='Фильтр по ФИО'),
            OpenApiParameter('position',   OpenApiTypes.STR,  description='Фильтр по должности'),
            OpenApiParameter('salary_min', OpenApiTypes.NUMBER, description='Зарплата от'),
            OpenApiParameter('salary_max', OpenApiTypes.NUMBER, description='Зарплата до'),
            OpenApiParameter('hired_from', OpenApiTypes.DATE,  description='Дата приёма с (YYYY-MM-DD)'),
            OpenApiParameter('hired_to',   OpenApiTypes.DATE,  description='Дата приёма до (YYYY-MM-DD)'),
            OpenApiParameter('search',     OpenApiTypes.STR,  description='Поиск по ФИО, email, должности'),
            OpenApiParameter('ordering',   OpenApiTypes.STR,  description='Сортировка: full_name | salary | hired_date'),
        ],
    ),
    create=extend_schema(
        tags=['employees'],
        summary='Создать сотрудника',
    ),
    retrieve=extend_schema(
        tags=['employees'],
        summary='Детали сотрудника',
    ),
    update=extend_schema(
        tags=['employees'],
        summary='Обновить сотрудника (полное)',
    ),
    partial_update=extend_schema(
        tags=['employees'],
        summary='Обновить сотрудника (частичное)',
    ),
    destroy=extend_schema(
        tags=['employees'],
        summary='Удалить сотрудника',
    ),
)
class EmployeeViewSet(viewsets.ModelViewSet):
    queryset           = Employee.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    filterset_class    = EmployeeFilter
    search_fields      = ('full_name', 'email', 'position')
    ordering_fields    = ('full_name', 'salary', 'hired_date', 'created_at')
    ordering           = ('-created_at',)

    def get_serializer_class(self):
        if self.action == 'list':
            return EmployeeListSerializer
        return EmployeeSerializer
