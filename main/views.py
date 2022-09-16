from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from main.models import Category, Task, Priority
from main.permissions import IsOwner
from main.serializers import CategorySerializer, TaskSerializer, PrioritySerializer

from main.services.get_category_statistic import get_all_statistic, get_statistic_by_category
from main.services.paginations import PaginationTasks


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = [IsOwner]
    filter_backends = [SearchFilter]
    search_fields = ['name']

    def get_queryset(self):
        return self.request.user.categories.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


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

        if category:
            return self.request.user.owner_tasks.filter(category__id=category)
        else:
            return self.request.user.owner_tasks.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user, is_done=False)

    @action(detail=False, methods=['get'])
    def get_incomplete(self, request):
        """
        Return all incomplete tasks count for current user
        """
        count = self.request.user.owner_tasks.filter(is_done=False).count()

        data = {
            'incomplete_count': f'{count}'
        }

        return Response(data)


class PriorityViewSet(viewsets.ModelViewSet):
    serializer_class = PrioritySerializer
    permission_classes = [IsOwner]

    def get_queryset(self):
        return self.request.user.owner_priority.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def create(self, request, *args, **kwargs):
        if Priority.objects.filter(name=request.data.get('name'), owner=request.user).exists():
            return Response('current priority exist')
        return super().create(request, *args, **kwargs)


class TaskStatistic(APIView):
    permission_classes = (IsOwner, )

    def get(self, request, category_id: int, format=None):

        if category_id == 0:
            """ Return statistic for all categories """
            data = get_all_statistic(request)
        else:
            """ Returning category statistics based on related tasks """
            category = get_object_or_404(Category, id=category_id)
            tasks_count = Task.objects.filter(category=category).count()
            data = get_statistic_by_category(category, tasks_count=tasks_count)

            """
            Calling a permission check before return Response
            """
            self.check_object_permissions(request, category)

        return Response(data)






