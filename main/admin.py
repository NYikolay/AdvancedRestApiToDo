from django.contrib import admin

from main.models import Category, Task, Priority

admin.site.register(Category)
admin.site.register(Task)
admin.site.register(Priority)
