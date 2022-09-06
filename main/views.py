from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from main.models import Category, Task
from main.permissions import IsOwner
from main.serializers import CategorySerializer, TaskSerializer, PrioritySerializer

import json

from main.services.get_category_statistic import get_all_statistic, get_statistic_by_category
from main.services.paginations import PaginationTasks


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
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ['is_done', 'priority']
    search_fields = ['name']
    ordering_fields = ['name', 'due_date', 'priority', 'category']
    pagination_class = PaginationTasks

    def get_queryset(self):
        """
        If the ?category=id parameter came in, it returns tasks depending
        on the current category otherwise it returns all tasks of the current user
        """
        category = self.request.query_params.get('category')
        is_done = self.request.query_params.get('is_done')
        priority = self.request.query_params.get('priority')
        if category:
            return Task.objects.filter(owner=self.request.user, category__id=category)
        elif is_done and priority is not None:
            return Task.objects.filter(owner=self.request.user, is_done=is_done, priority=priority)
        elif is_done is not None:
            return Task.objects.filter(owner=self.request.user, is_done=is_done)
        elif priority is not None:
            return Task.objects.filter(owner=self.request.user, priority=priority)
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
    permission_classes = (IsOwner, )

    def get(self, request, category_id: int, format=None):

        if category_id == 0:
            """ Return statistic for all categories """
            data = get_all_statistic(request)
        else:
            """ Returning category statistics based on related tasks """
            category = get_object_or_404(Category, id=category_id)
            tasks = Task.objects.filter(category=category).count()
            data = get_statistic_by_category(category, tasks_count=tasks)

            """
            Calling a permission check before return Response
            """
            self.check_object_permissions(request, category)

        return Response(data)






