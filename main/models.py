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
        """
        Returns incomplete tasks related to the Category object
        """
        return Task.objects.filter(category__id=self.id, is_done=False).count()

    def get_completed_tasks(self):
        """
        Returns completed tasks related to the Category object
        """
        return Task.objects.filter(category__id=self.id, is_done=True).count()


class Priority(models.Model):
    name = models.CharField(max_length=256, default='Без приоритета', verbose_name='Приоритет задачи')
    owner = models.ForeignKey(CustomUser,
                              on_delete=models.CASCADE,
                              related_name='owner_priority',
                              verbose_name='Владелец приоритета')
    color = models.CharField(max_length=7, null=True, verbose_name='Цвет приоритета')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Приоритет'
        verbose_name_plural = 'Приоритеты'
        ordering = ['name']


class Task(models.Model):
    """
    Model for todo task
    """

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
    priority = models.ForeignKey(Priority,
                                 on_delete=models.SET_NULL,
                                 null=True,
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

    def get_incomplete_tasks(self):
        count = Task.objects.filter(category__id=self.id, is_done=False).count()

        return count


