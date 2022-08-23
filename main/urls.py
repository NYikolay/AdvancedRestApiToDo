from django.contrib import admin
from django.urls import path
from rest_framework import routers

from main.views import CategoryViewSet, TaskViewSet

router = routers.DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='categories')
router.register(r'tasks', TaskViewSet, basename='tasks')

urlpatterns = [
]

urlpatterns += router.urls
