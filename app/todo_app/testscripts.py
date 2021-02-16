import os
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from rest_framework.test import APIClient
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.test import RequestsClient
from todo_app.models import ToDoApp
from django.contrib.auth import authenticate
import todo_server_app.settings as settings
from dotenv import load_dotenv
from rest_framework_api_key.models import APIKey
# 'rest_framework.authentication.TokenAuthentication',


# client = RequestsClient()
# response = client.get('http://localhost:8000/todoapp/api/list/',headers={'Authorization': 'Api-Key fhA9DGBN.9HOxWVSGw9KlbVHuAY6HbdH9aQqCR6Vh'})

# user = User.objects.create_user(
#     username=data['email'],
#     email=data['email'],
#     first_name=data['first_name'] if data['first_name'] != "" else "",
#     last_name=data['last_name'] if data['last_name'] != "" else "",
#     is_active=True,
# )
# user.set_password(data['password'])
# user.save()

class TestScript:

    def __init__(self):
        self.username = ""
        self.email = ""
        self.first_name = ""
        self.last_name = ""
        self.is_active = False

    def create_user(self, username, password, email, first_name, last_name):
        if password == "":
            msg = _('Password must not be empty')
            raise ValidationError({'error':msg})
        else:
            self.username = username
            self.email = email
            self.first_name = first_name
            self.last_name = last_name
            self.is_active = True
            user = User.objects.create_user(
                username=username,
                email=email,
                first_name=first_name,
                last_name=last_name,
                is_active=True,
            )
            user.set_password(password)
            user.save()
            api_key = os.environ.get(username)
            return Response({'api_key':api_key})
    
    def retrieve_key(self, username, password):
        if username == "" or password == "":
            msg = _('Username and password must not be empty.')
            raise ValidationError({'error':msg})
        else:
            user = authenticate(username=username, password=password)
            if user is None:
                msg = _('Username and password do not match.')
                raise ValidationError({'error':msg})
            else:
                api_key = os.environ.get(user.username)
                if api_key is None:
                    load_dotenv(os.path.join(settings.BASE_DIR, '.apikey'))
                    api_key = os.environ.get(user.username)
                return Response({'api_key':api_key})
    
    def create_todo(self, api_key, task_title, task_description, task_state, task_due_date):
        if api_key == "":
            msg = _('API Key must not be empty.')
            raise ValidationError({'error':msg})
        else:
            # key = APIKey.objects.get_from_key(api_key)
            # user = User.objects.get(id=int(key.name))
            client = RequestsClient()
            data = {
                'task_title': task_title,
                'task_description': task_description,
                'task_state': task_state,
                'task_due_date': task_due_date,
            }
            try:
                response = client.post('http://localhost:8000/todoapp/api/create/', data, headers={'Authorization': 'Api-Key %s' % api_key })
                return Response(response.content)
            except Exception as e:
                raise ValidationError({'error':e.args})
            
            
    def update_todo(self, api_key, todo_id, task_title, task_description, task_state, task_due_date):
        if api_key == "":
            msg = _('API Key must not be empty.')
            raise ValidationError({'error':msg})
        else:
            client = RequestsClient()
            data = {
                'task_title': task_title,
                'task_description': task_description,
                'task_state': task_state,
                'task_due_date': task_due_date,
            }
            try:
                response = client.put('http://localhost:8000/todoapp/api/update/%s/' % todo_id, data, headers={'Authorization': 'Api-Key %s' % api_key })
                return Response(response.content)
            except Exception as e:
                raise ValidationError({'error':e.args})
            
    def delete_todo(self, api_key, todo_id):
        if api_key == "":
            msg = _('API Key must not be empty.')
            raise ValidationError({'error':msg})
        else:
            client = RequestsClient()
            try:
                response = client.delete('http://localhost:8000/todoapp/api/delete/%s/' % todo_id, headers={'Authorization': 'Api-Key %s' % api_key })
                return Response(response.content)
            except Exception as e:
                raise ValidationError({'error':e.args})
# from todo_app.testscripts import TestScript
# a = TestScript()
# response = a.update_todo('aqJADdwS.NN8SG8KaWm00o3fYRdse6xYUmaMeXcMI', '12', 'adf do this','mama','1','2021-02-16')
# response = a.create_todo('aqJADdwS.NN8SG8KaWm00o3fYRdse6xYUmaMeXcMI', 'hello do','mama miya','2','2021-02-15')
# response = a.retrieve_key('abcde','hello123456')
# a.create_user('abcde','hello123456','e3studio@gmail.com','lewis','chen')
