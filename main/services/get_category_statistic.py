from django.http import HttpRequest
from rest_framework.generics import get_object_or_404

from main.models import Task, Category


def get_all_statistic(request: HttpRequest) -> dict:
    """
    Returns statistics for all categories of the current user
    """
    tasks = Task.objects.filter(owner=request.user).count()

    completed_tasks = Task.objects.filter(owner=request.user, is_done=True).count()
    incompleted_tasks = Task.objects.filter(owner=request.user, is_done=False).count()

    completed_percent = int((completed_tasks / tasks) * 100)
    incompleted_percent = int((incompleted_tasks / tasks) * 100)

    data = {
        'tasks_count': tasks,
        'completed_tasks': completed_tasks,
        'incompleted_tasks': incompleted_tasks,
        'completed_percent': completed_percent,
        'incompleted_percent': incompleted_percent
    }

    return data


