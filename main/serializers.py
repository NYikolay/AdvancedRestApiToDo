from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password

from main.models import Category, Task, Priority


class CategorySerializer(serializers.ModelSerializer):
    get_incomplete_tasks = serializers.ReadOnlyField()

    class Meta:
        model = Category
        fields = ['name', 'id', 'get_incomplete_tasks']
        read_only_fields = ('id',)


class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'owner')


class PrioritySerializer(serializers.ModelSerializer):

    class Meta:
        model = Priority
        fields = '__all__'
        read_only_fields = ('id', 'owner')

