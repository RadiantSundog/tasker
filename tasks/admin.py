from django.contrib import admin
from tasks.models import Task

# Register your models here.


@admin.register(Task)
class TasksAdmin(admin.ModelAdmin):
    pass
