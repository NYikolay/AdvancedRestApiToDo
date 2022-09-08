from rest_framework import serializers
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

    def validate(self, attrs):
        """
        If a priority is created or updated, it checks for the existence of the name in the database
        """
        request = self.context.get('request')
        if attrs.get('name'):
            if Priority.objects.filter(name=attrs['name'], owner=request.user).exists():
                raise serializers.ValidationError({
                    'name': 'Current priority name is exist'
                })
        return attrs
