from django.contrib import admin
from .models import Task


class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'priority', 'user', 'completed')
    search_fields = ('title', 'description')
    list_filter = ('priority', 'completed')


admin.site.register(Task, TaskAdmin)
