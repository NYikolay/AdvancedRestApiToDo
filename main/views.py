from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from main.models import Category, Task
from main.permissions import IsOwner
from main.serializers import CategorySerializer, TaskSerializer, PrioritySerializer

import json


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = [IsOwner]
    filter_backends = [SearchFilter]
    search_fields = ['name']

    def get_queryset(self):
        return self.request.user.categories.all()


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsOwner]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filter_fields = ['is_done', 'priority']
    search_fields = ['name']

    def get_queryset(self):
        """
        If the ?category=id parameter came in, it returns tasks depending
        on the current category otherwise it returns all tasks of the current user
        """
        category = self.request.query_params.get('category')
        if category:
            return Task.objects.filter(owner=self.request.user, category__id=category)
        else:
            return self.request.user.owner_tasks.all()

    @action(detail=False, methods=['get'])
    def get_incomplete(self, request):
        """
        Return all incomplete tasks for current user
        """
        count = Task.objects.filter(owner=self.request.user, is_done=False).count()

        data = {
            'incomplete_count': f'{count}'
        }

        return Response(data)


class PriorityViewSet(viewsets.ModelViewSet):
    serializer_class = PrioritySerializer
    permission_classes = [IsOwner]

    def get_queryset(self):
        return self.request.user.owner_priority.all()


class TaskStatistic(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        current_category = request.query_params.get("category", None)
        try:
            tasks = Task.objects.filter(category_id=current_category).count()
            tasks_done = Task.objects.filter(category_id=current_category, is_done=True).count()
            incompleted_tasks = Task.objects.filter(category_id=current_category, is_done=False).count()
        except Task.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        data = {
            'tasks_count': tasks,
            'tasks_done': tasks_done,
            'incompleted_tasks': incompleted_tasks
        }

        return Response(data)






