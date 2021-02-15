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
    RetrieveAPIView,
    CreateAPIView,
    UpdateAPIView,
    DestroyAPIView,
)
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response

from rest_framework.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
# from rest_auth.models import TokenModel
# from sgback.models import OrderID, OrderInfo, Priority, OrderStatus, OrderType, OrderExtra, ActionItem, AdditionalTestType, AdditionalTestStatus, Status
# from sgback.models import MTABatch, YABatch

# user and staff from sguser models
from todo_app.models import ToDoApp, UserAPIKey
from .serializers import ToDoCreateSerializer, ToDoUpdateSerializer


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


