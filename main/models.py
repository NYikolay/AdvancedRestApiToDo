from django.db import models
from django.utils.translation import gettext_lazy as _

from accounts.models import CustomUser


class Category(models.Model):
    """
    Model for category
    """

    name = models.CharField(max_length=255, verbose_name='Название категории')
    owner = models.ForeignKey(CustomUser,
                              on_delete=models.CASCADE,
                              related_name='categories',
                              verbose_name='Владелец категории')
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']

    def get_incomplete_tasks(self):
        count = Task.objects.filter(category__id=self.id, is_done=False).count()

        return count


class Task(models.Model):
    """
    Model for todo task
    """

    class Priority(models.TextChoices):
        NOPR = 'Без приоритета', _('Без приоритета')
        LOW = 'Низкий', _('Низкий')
        MEDIUM = 'Средний', _('Средний')
        HIGH = 'Высокий', _('Высокий')
        URGENT = 'Очень срочно', _('Очень срочно')

    owner = models.ForeignKey(CustomUser,
                              on_delete=models.CASCADE,
                              related_name='owner_tasks',
                              verbose_name='Владелец задания')
    name = models.CharField(max_length=625, verbose_name='Название задания')
    category = models.ForeignKey(Category,
                                 on_delete=models.SET_NULL,
                                 null=True,
                                 related_name='tasks',
                                 verbose_name='Категория задания')
    priority = models.CharField(max_length=56,
                                choices=Priority.choices,
                                default=Priority.NOPR,
                                verbose_name='Приоритет задачи')
    due_date = models.DateField('Срок выполнения')
    is_done = models.BooleanField('Выполнено ли задание')
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Владелец {self.owner.email}, название {self.name}'

    class Meta:
        verbose_name = 'Задание'
        verbose_name_plural = 'Задания'
        ordering = ['-created_at']


