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
        fields = '__all__'

class ToDoDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ToDoApp
        fields = '__all__'

class ToDoListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ToDoApp
        fields = '__all__'

class ToDoRetrieveSerializer(serializers.Serializer):
    choices = ['task_id','user_id','task_title','task_description','task_state','task_due_date']
    todo_list = ToDoApp.objects.all()
    titles = [item.task_title for item in todo_list.order_by('task_title').distinct('task_title')]
    descriptions = [item.task_description for item in todo_list.order_by('task_description').distinct('task_description')]
    states = (
        ('1', 'Todo'),
        ('2', 'In Progress'),
        ('3', 'Done'),
    )
    due_dates = [item.task_due_date for item in todo_list.order_by('task_due_date').distinct('task_due_date')]
    user_list = [item.user_id for item in todo_list]
    
    sort_by = serializers.ChoiceField(choices, allow_blank=True)
    filter_title_by = serializers.ChoiceField(titles, allow_blank=True)
    filter_description_by = serializers.ChoiceField(descriptions, allow_blank=True)
    filter_state_by = serializers.ChoiceField(states, allow_blank=True)
    filter_due_date_by = serializers.ChoiceField(due_dates, allow_blank=True)
    filter_user_by = serializers.ChoiceField(user_list, allow_blank=True)
    reverse_order = serializers.BooleanField(default=False)

    def update(self, instance, validated_data):
        instance.sort_by = validated_data.get(
            'sort_by', instance.sort_by)
        instance.filter_title_by = validated_data.get(
            'filter_title_by', instance.filter_title_by)
        instance.filter_description_by = validated_data.get(
            'filter_description_by', instance.filter_description_by)
        instance.filter_state_by = validated_data.get(
            'filter_state_by', instance.filter_state_by)
        instance.filter_due_date_by = validated_data.get(
            'filter_due_date_by', instance.filter_due_date_by)
        instance.filter_user_by = validated_data.get(
            'filter_user_by', instance.filter_user_by)
        instance.reverse_order = validated_data.get(
            'reverse_order', instance.reverse_order)
        instance.save()
        return instance
    

