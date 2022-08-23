from django.shortcuts import render
from rest_framework import viewsets

from main.models import Category
from main.permissions import IsOwner
from main.serializers import CategorySerializer, TaskSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = [IsOwner]

    def get_queryset(self):
        return self.request.user.categories.all()


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsOwner]

    def get_queryset(self):
        return self.request.user.owner_tasks.all()

