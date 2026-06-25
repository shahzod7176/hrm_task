from django.db import models
from apps.employees.models import Employee


class Task(models.Model):

    class Status(models.TextChoices):
        CREATED     = 'created',     'Создана'
        IN_PROGRESS = 'in_progress', 'В работе'
        DONE        = 'done',        'Выполнена'

    title       = models.CharField('Название', max_length=255)
    description = models.TextField('Описание', blank=True)
    employee    = models.ForeignKey(
        Employee,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='tasks',
        verbose_name='Сотрудник',
    )
    status      = models.CharField(
        'Статус', max_length=20,
        choices=Status.choices,
        default=Status.CREATED,
    )
    due_date    = models.DateField('Срок выполнения', null=True, blank=True)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name        = 'Задача'
        verbose_name_plural = 'Задачи'
        ordering            = ['-created_at']

    def __str__(self):
        return f'{self.title} [{self.get_status_display()}]'
