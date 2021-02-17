from django.contrib import admin

# Register your models here.

from .models import ToDoApp, UserAPIKey


@admin.register(ToDoApp)
class ToDoAppAdmin(admin.ModelAdmin):
    list_display = ('task_id', 'user_id', 'task_title',
                    'task_description', 'task_state', 'task_due_date')


@admin.register(UserAPIKey)
class UserAPIKeyAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'api_key')
