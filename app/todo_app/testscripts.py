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
            client = RequestsClient()
            data = {
                'username': username,
                'password': password,
                'first_name': first_name,
                'last_name': last_name,
                'email': email,    
            }
            try:
                response = client.post('http://localhost:8000/todoapp/api/createuser/', data)
                return response.data
            except Exception as e:
                raise ValidationError({'error':e.args})

    
    def retrieve_key(self, username, password):
        if username == "" or password == "":
            msg = _('Username and password must not be empty.')
            raise ValidationError({'error':msg})
        else:
            client = RequestsClient()
            data = {
                'username': username,
                'password': password
            }
            try:
                response = client.post('http://localhost:8000/todoapp/api/getapikey/', data)
                return response.data
            except Exception as e:
                raise ValidationError({'error':e.args})
    
    def create_todo(self, api_key, task_title, task_description, task_state, task_due_date):
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
                response = client.post('http://localhost:8000/todoapp/api/create/', data, headers={'Authorization': 'Api-Key %s' % api_key })
                return response
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
                return response
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
                return response
            except Exception as e:
                raise ValidationError({'error':e.args})
    
    def list_options(self, api_key):
        if api_key == "":
            msg = _('API Key must not be empty.')
            raise ValidationError({'error':msg})
        else:
            client = RequestsClient()
            try:
                response = client.post('http://localhost:8000/todoapp/api/options/', headers={'Authorization': 'Api-Key %s' % api_key })
                return response.content
            except Exception as e:
                raise ValidationError({'error':e.args})

    def list_todo(self, api_key, action, sort_by, filter_title_by, filter_description_by, filter_state_by, filter_due_date_by, reverse_order):
        if api_key == "":
            msg = _('API Key must not be empty.')
            raise ValidationError({'error':msg})
        else:
            if action == 'get':
                response = client.get('http://localhost:8000/todoapp/api/list/', headers={'Authorization': 'Api-Key %s' % api_key })
                return response
            else:
                client = RequestsClient()
                try:
                    sort_choices = ['task_title','task_description','task_state','task_due_date']
                    data = {
                        "sort_by": sort_by,
                        "filter_title_by": filter_title_by,
                        "filter_description_by": filter_description_by,
                        "filter_state_by": filter_state_by,
                        "filter_due_date_by": filter_due_date_by,
                        "reverse_order": reverse_order,
                    }
                    response = client.post('http://localhost:8000/todoapp/api/list/', data, headers={'Authorization': 'Api-Key %s' % api_key })
                    return response
                except Exception as e:
                    raise ValidationError({'error':e.args})

# from todo_app.testscripts import TestScript
# a = TestScript()
# response = a.create_todo('aqJADdwS.NN8SG8KaWm00o3fYRdse6xYUmaMeXcMI', 'hello do','mama miya','2','2021-02-15')
# response = a.update_todo('aqJADdwS.NN8SG8KaWm00o3fYRdse6xYUmaMeXcMI', '12', 'adf do this','mama','1','2021-02-16')
# response = a.list_options('aqJADdwS.NN8SG8KaWm00o3fYRdse6xYUmaMeXcMI')
# response = a.list_todo('aqJADdwS.NN8SG8KaWm00o3fYRdse6xYUmaMeXcMI','task_title','','','','', False)
# response = a.delete_todo('aqJADdwS.NN8SG8KaWm00o3fYRdse6xYUmaMeXcMI', '12')
# response = a.retrieve_key('abcde','hello123456')
# a.create_user('abcde','hello123456','e3studio@gmail.com','lewis','chen')

# from rest_framework.test import RequestsClient
# client = RequestsClient()
# user_data = {
#     'username': username,
#     'password': password,
#     'first_name': first_name,
#     'last_name': last_name,
#     'email': email,    
# }
# response = client.post('http://localhost:8000/todoapp/api/createuser/', user_data)
# credentials = {
#     'username': username,
#     'password': password
# }
# response = client.post('http://localhost:8000/todoapp/api/getapikey/', credentials)
# obtain your api_key and assign it to api_key
# api_key = 'aqJADdwS.NN8SG8KaWm00o3fYRdse6xYUmaMeXcMI'
# todo_data = {
#     'task_title': task_title,
#     'task_description': task_description,
#     'task_state': task_state,
#     'task_due_date': task_due_date,
# }
# response = client.post('http://localhost:8000/todoapp/api/create/', todo_data, headers={'Authorization': 'Api-Key %s' % api_key })
# to update or delete a todo item, we need to remember its todo_id
# todo_id = 1
# response = client.post('http://localhost:8000/todoapp/api/update/%s/' % todo_id, todo_data, headers={'Authorization': 'Api-Key %s' % api_key })
# response = client.post('http://localhost:8000/todoapp/api/delete/%s/' % todo_id, headers={'Authorization': 'Api-Key %s' % api_key })
# response = client.get('http://localhost:8000/todoapp/api/list/', headers={'Authorization': 'Api-Key %s' % api_key })
# response = client.post('http://localhost:8000/todoapp/api/options/', headers={'Authorization': 'Api-Key %s' % api_key })
# option_data = {
#     "sort_by": sort_by,
#     "filter_title_by": filter_title_by,
#     "filter_description_by": filter_description_by,
#     "filter_state_by": filter_state_by,
#     "filter_due_date_by": filter_due_date_by,
#     "reverse_order": reverse_order,
# }
# response = client.post('http://localhost:8000/todoapp/api/list/', option_data, headers={'Authorization': 'Api-Key %s' % api_key })