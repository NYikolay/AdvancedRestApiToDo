from django.db.models import Count
from django.http import HttpRequest
from rest_framework.generics import get_object_or_404

from main.models import Task, Category


def get_all_statistic(request: HttpRequest) -> dict:
    """
    Returns statistics for all categories of the current user
    """
    tasks = request.user.owner_tasks.values('is_done').annotate(count=Count('is_done'))

    completed_tasks = 0
    incompleted_tasks = 0

    for item in tasks:
        if item.get('is_done'):
            completed_tasks = item.get('count')
        else:
            incompleted_tasks = item.get('count')

    tasks_count = completed_tasks + incompleted_tasks

    if completed_tasks > 0:
        completed_percent = int((completed_tasks / tasks_count) * 100)
    else:
        completed_percent = 0

    if incompleted_tasks > 0:
        incompleted_percent = int((incompleted_tasks / tasks_count) * 100)
    else:
        incompleted_percent = 0

    data = {
        'tasks_count': tasks_count,
        'completed_tasks': completed_tasks,
        'incompleted_tasks': incompleted_tasks,
        'completed_percent': completed_percent,
        'incompleted_percent': incompleted_percent
    }

    return data


def get_statistic_by_category(category, tasks_count: int) -> dict:
    if category.get_completed_tasks() > 0:
        completed_percent = int((category.get_completed_tasks() / tasks_count) * 100)
    else:
        completed_percent = 0
    if category.get_incomplete_tasks() > 0:
        incompleted_percent = int((category.get_incomplete_tasks() / tasks_count) * 100)
    else:
        incompleted_percent = 0

    data = {
        'tasks_count': tasks_count,
        'completed_tasks': category.get_completed_tasks(),
        'incompleted_tasks': category.get_incomplete_tasks(),
        'completed_percent': completed_percent,
        'incompleted_percent': incompleted_percent
    }

    return data


