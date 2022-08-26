from django.shortcuts import render
from rest_framework import viewsets, filters

from main.models import Category, Task
from main.permissions import IsOwner
from main.serializers import CategorySerializer, TaskSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = [IsOwner]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

    def get_queryset(self):
        return self.request.user.categories.all()


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsOwner]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

    def get_queryset(self):
        try:
            category = self.request.query_params.get('category')
            queryset = Task.objects.filter(owner=self.request.user, category__id=category)
        except:
            queryset = self.request.user.owner_tasks.all()

        return queryset

