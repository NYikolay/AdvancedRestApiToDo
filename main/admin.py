from django.contrib import admin

from main.models import Category, Task, Priority

admin.site.register(Task)
admin.site.register(Priority)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
