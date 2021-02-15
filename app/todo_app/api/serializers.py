from rest_framework import serializers
from todo_app.models import ToDoApp
from django.utils.translation import ugettext_lazy as _


class ToDoCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ToDoApp
        fields = ('task_title','task_description','task_state','task_due_date')


class ToDoUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ToDoApp
        fields = ('task_id','task_title','task_description','task_state','task_due_date')