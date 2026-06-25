from django.db import models


class Employee(models.Model):
    full_name  = models.CharField('ФИО', max_length=255)
    phone      = models.CharField('Телефон', max_length=20, unique=True)
    email      = models.EmailField('Email', unique=True)
    position   = models.CharField('Должность', max_length=150)
    salary     = models.DecimalField('Зарплата', max_digits=12, decimal_places=2)
    hired_date = models.DateField('Дата приёма')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name        = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'
        ordering            = ['-created_at']

    def __str__(self):
        return f'{self.full_name} — {self.position}'
