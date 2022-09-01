from django.contrib import admin
from django.urls import path
from rest_framework import routers

from main.views import CategoryViewSet, TaskViewSet, PriorityViewSet, TaskStatistic

router = routers.DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='categories')
router.register(r'tasks', TaskViewSet, basename='tasks')
router.register(r'priorities', PriorityViewSet, basename='priorities')

urlpatterns = [
    path('category_statistic/', TaskStatistic.as_view())
]

urlpatterns += router.urls
