import datetime
import calendar
from django.contrib.sites.models import Site
from django.db.models import Q, F
from itertools import chain
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.conf import settings
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import (
    GenericAPIView,
    ListAPIView,
    ListCreateAPIView,
    RetrieveAPIView,
    CreateAPIView,
    UpdateAPIView,
    DestroyAPIView,
)
from rest_framework.response import Response

from rest_framework.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from todo_app.models import ToDoApp, UserAPIKey
from .serializers import ToDoCreateSerializer, ToDoUpdateSerializer, ToDoDeleteSerializer, ToDoListSerializer, ToDoRetrieveSerializer


def auth_proceed(token):
    try:
        api_key = UserAPIKey.objects.get(api_key=token)
    except UserAPIKey.DoesNotExist:
        msg = _('You are not registered.')
        raise ValidationError({'error': msg})
    else:
        return api_key

class TodoCreateView(CreateAPIView):
    queryset = ToDoApp.objects.all()
    serializer_class = ToDoCreateSerializer
    permission_classes = (AllowAny, )

    def get(self, request, format=None):
        # token = request.headers['Authorization'].split('Token ')[1]
        token = '123'
        api_key = auth_proceed(token)
        if api_key is not None:
            return Response('Hello. How are you?')

    def post(self, request, format=None):
        # token = request.headers['Authorization'].split('Token ')[1]
        token = '123'
        api_key = auth_proceed(token)
        if api_key is not None:
            data = request.data
            user = api_key.user_id
            try:
                todo_obj, created = ToDoApp.objects.get_or_create(
                    user_id = user,
                    defaults={
                        'task_title': data['task_title'],
                        'task_description': data['task_description'],
                        'task_state': data['task_state'],
                        'task_due_date': data['task_due_date']
                    }
                )
                return Response({'message':'Item is created'})
            except Exception as e:
                todo_obj = ToDoApp.objects.create(task_title=data['task_title'])
                todo_obj.user_id = user
                todo_obj.task_description = data['task_description']
                todo_obj.task_state = data['task_state']
                todo_obj.task_due_date = data['task_due_date']
                todo_obj.save()
                return Response({'message':'Item is created'})
            

class TodoUpdateView(UpdateAPIView):
    queryset = ToDoApp.objects.all()
    serializer_class = ToDoUpdateSerializer
    permission_classes = (AllowAny, )

    def get(self, request, key, format=None):
        # token = request.headers['Authorization'].split('Token ')[1]
        token = '123'
        api_key = auth_proceed(token)
        if api_key is not None:
            return Response('Hello. How are you?')
    
    def put(self, request, key, format=None):
        # token = request.headers['Authorization'].split('Token ')[1]
        token = '123'
        api_key = auth_proceed(token)
        if api_key is not None:
            data = request.data
            try:
                todo = ToDoApp.objects.get(task_id=key)
            except ToDoApp.DoesNotExist:
                msg = _('This item is not yet created.')
                raise ValidationError({'error': msg})
            else:
                todo_obj, created = ToDoApp.objects.update_or_create(
                    task_id = todo.task_id,
                    defaults={
                        'task_title': data['task_title'],
                        'task_description': data['task_description'],
                        'task_state': data['task_state'],
                        'task_due_date': data['task_due_date']
                    }
                )
                return Response({'message':'Item is updated'})

class TodoDeleteView(DestroyAPIView):
    queryset = ToDoApp.objects.all()
    serializer_class = ToDoDeleteSerializer
    permission_classes = (AllowAny, )

    def get(self, request, key, format=None):
        # token = request.headers['Authorization'].split('Token ')[1]
        token = '123'
        api_key = auth_proceed(token)
        if api_key is not None:
            return Response('Hello. How are you?')
    
    def delete(self, request, key, format=None):
        # token = request.headers['Authorization'].split('Token ')[1]
        token = '123'
        api_key = auth_proceed(token)
        if api_key is not None:
            data = request.data
            try:
                todo = ToDoApp.objects.get(task_id=key)
            except ToDoApp.DoesNotExist:
                msg = _('This item is not yet created.')
                raise ValidationError({'error': msg})
            else:
                todo.delete()
                return Response({'message':'Item is deleted'})
from functools import reduce
import operator

class TodoListView(ListCreateAPIView):
    queryset = ToDoApp.objects.all()
    serializer_class = ToDoRetrieveSerializer
    permission_classes = (AllowAny, )

    def get(self, request, format=None):
        # token = request.headers['Authorization'].split('Token ')[1]
        token = '123'
        api_key = auth_proceed(token)
        if api_key is not None:
            todo_list = ToDoApp.objects.all()
            serializer = ToDoListSerializer(todo_list, many=True)
            serializer_data = serializer.data
            return Response(serializer_data)
    
    def post(self, request, format=None):
        # token = request.headers['Authorization'].split('Token ')[1]
        token = '123'
        api_key = auth_proceed(token)
        if api_key is not None:
            data = request.data
            try:
                todo = ToDoApp.objects.all()
            except ToDoApp.DoesNotExist:
                msg = _('No item is yet created.')
                raise ValidationError({'error': msg})
            else:
                cc = []
                if data["filter_title_by"] != "":
                    cc.append(Q(task_title=data["filter_title_by"]))
                if data["filter_description_by"] != "":
                    cc.append(Q(task_description=data["filter_description_by"]))
                if data["filter_state_by"] != "":
                    cc.append(Q(task_state=data["filter_state_by"]))
                if data["filter_due_date_by"] != "":
                    cc.append(Q(task_due_date=data["filter_due_date_by"]))
                if data["filter_user_by"] != "":
                    cc.append(Q(user_id__username=data["filter_user_by"]))
                # Split into two actions: any of the above is not empty or empty
                sort_choices = ['user_id','task_title','task_description','task_state','task_due_date']
                if len(cc) != 0:
                    info_cc = ToDoApp.objects.filter(reduce(operator.and_, cc))
                else:
                    info_cc = ToDoApp.objects.all()
                if data['sort_by'] in sort_choices and 'reverse_order' in data.keys():
                    info_cc = info_cc.order_by('-%s' % data['sort_by'], '-%s' % data['sort_by'])
                elif data['sort_by'] in sort_choices and 'reverse_order' not in data.keys():
                    info_cc = info_cc.order_by(data['sort_by'], data['sort_by'])
                elif data['sort_by'] not in sort_choices and 'reverse_order' in data.keys():
                    info_cc = info_cc.order_by('-task_id')
                elif data['sort_by'] not in sort_choices and 'reverse_order' not in data.keys():
                    info_cc = info_cc.order_by('task_id')
                elif data['sort_by'] == 'task_id' and 'reverse_order' in data.keys():
                    info_cc = info_cc.order_by('-task_id')
                serializer = ToDoListSerializer(info_cc, many=True)
                serializer_data = serializer.data
                return Response(serializer_data)
