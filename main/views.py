from django.shortcuts import render

from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response

from main.models import Category, Task
from main.permissions import IsOwner
from main.serializers import CategorySerializer, TaskSerializer

import json


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = [IsOwner]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

    def get_queryset(self):
        return self.request.user.categories.all()


class TaskViewSet(viewsets.ModelViewSet):
    """
    Depending on the category query, ?category=id returns linked jobs
    """
    serializer_class = TaskSerializer
    permission_classes = [IsOwner]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

    def get_queryset(self):
        category = self.request.query_params.get('category')
        if category:
            return Task.objects.filter(owner=self.request.user, category__id=category)
        else:
            return self.request.user.owner_tasks.all()

    @action(detail=False, methods=['get'])
    def get_incomplete(self, request):
        count = Task.objects.filter(owner=self.request.user, is_done=False).count()

        data = {
            'incomplete_count': f'{count}'
        }

        return Response(data)



