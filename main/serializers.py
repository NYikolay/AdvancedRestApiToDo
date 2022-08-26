from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password

from main.models import Category, Task


class CategorySerializer(serializers.ModelSerializer):
    get_incomplete_tasks = serializers.ReadOnlyField()

    class Meta:
        model = Category
        fields = ['name', 'id', 'get_incomplete_tasks']
        read_only_fields = ('id',)

    def create(self, validated_data):
        request = self.context.get('request')
        category = Category.objects.create(
            name=validated_data['name'],
            owner=request.user
        )

        category.save()
        return category


class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'owner', 'is_done')

    def create(self, validated_data):
        request = self.context.get('request')
        category = Task.objects.create(
            name=validated_data['name'],
            owner=request.user,
            category=validated_data['category'],
            priority=validated_data['priority'],
            due_date=validated_data['due_date'],
            is_done=False,
        )

        category.save()
        return category
