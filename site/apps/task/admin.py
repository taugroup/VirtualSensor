from django.contrib import admin
from apps.task.models import Task


# Register your models here.
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    model = Task