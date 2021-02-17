# ToDoApp with Django PostgreSQL Docker and Nginx

For this project, we have three primary tasks. First, we will create a TODO server app with Django, PostgreSQL and Docker. The primary interface is a REST API, and we will provide an admin dashboard using Django’s Admin Site system for backend management. Next, we will configure the app to run on a Gunicorn WSGI server, behind an NGINX instance acting as a reverse-proxy. All components — Django/Gunicorn, Postgres, NGINX — will be deployed as Docker containers via docker-compose comands (i.e, docker-compose up should bring up the entire system and docker-compose down to shut everything down). Finally, we will provide Python script to test ToDoApp's REST API as a normal user. 

## Installation

To use the ToDoApp, you are required to install Python PostgreSQL and Docker on your system. Please click on the links below to redirect to corresponding websites, download installation packages and make sure these softwares are properly installed on your system.
1. [Python](https://www.python.org/)
2. [PostgreSQL](https://www.postgresql.org/)
3. [Docker](https://www.docker.com/)

## Pull Repository

To pull this repository, you need to have [Github](https://desktop.github.com/) installed in your system. After Github is installed, create any folder (i.e., workfolder) on your system, go to this folder and pull this repository.
```bash
$ mkdir workfolder
$ cd workfolder
$ git init
$ git remote add origin https://github.com/Lcyc29/todo_server_app.git
```

## Local Configuration

If you want to use Docker only, you can skip this part and jump to [Docker Configuration](#docker-configuration). Once the repository is successfully pulled to your folder, take a look at the structure of this folder. 
```bash
workfolder
│   .env.dev
│   .env.prod
│   .env.prod.db
│   .gitignore
│   docker-compose.prod.yml
│   docker-compose.yml
│   README.md
├───app
│   │   .apikey
│   │   .dockerignore
│   │   .envdev
│   │   Dockerfile
│   │   Dockerfile.prod
│   │   entrypoint.prod.sh
│   │   entrypoint.sh
│   │   manage.py
│   │   requirements.txt
│   ├───.vscode
│   ├───frontend
│   ├───todo_app
│   └───todo_server_app
└───nginx
```
The entire project is located inside ───app folder. Within this folder, ───todo_server_app is the main Django folder that manages the project. ───todo_app is where our app lives. There is also a folder called ───frontend, which is to build frontend webpages using ReactJS. ───nginx controls how the project is served in production via Docker container. In order to use ToDoApp locally on your system (not Docker container), you need to install Python's dependencies and virtual environment (VE). Depending on your system, you will setup the VE differently on Windows, MacOS or Ubuntu. Have a look at the links provided below for how to install and use Python virual environments on various systems.
1. [Python VE on Windows](https://docs.python.org/3/tutorial/venv.html) 
2. [Python VE on MacOS](https://sourabhbajaj.com/mac-setup/Python/virtualenv.html)
3. [Python VE on Ubuntu](https://www.linode.com/docs/guides/create-a-python-virtualenv-on-ubuntu-18-04/)

There are generally two ways to use VE, but it is recommended that you create the VE folder inside your project and add .gitignore to avoid pushing this folder to your repository, because this folder is very large. Once Python virtual environemnt is installed, go to ───app folder and create a VE folder (i.e., env). Activate your VE and install python dependencies from the "requirements.txt" file.
```bash
$ cd app
(Windows)
$ python -m venv env 
$ env/scripts/activate 
(MacOS)
$ python3 -m venv env (on MacOS)
$ source env/bin/activate
(Ubuntu)
$ virtualenv --python=python3 env (on Ubuntu)
$ source env/bin/activate

$ pip install -r requirements.txt
```
Once all dependencies are install, you need to configure PostgreSQL using specific username, password and database prior to using the app.
- Username: todo_app
- Password: todo_app
- Database: todo_app_dev
```postgres
#\ CREATE USER todo_app WITH PASSWORD 'todo_app';
#\ CREATE DATABASE todo_app_dev OWNER todo_app;
```
Once PosgreSQl is configured, you will first create a superuser for Django Admin Dashboard; otherwise, you are not allowed to use the Admin. Run the following command and enter your username, password and email for the superuser.
```bash
$ python manage.py createsuperuser
```
Before you can run the app in development, collect static files for Django from /app/frontend/build folder and create the PostgreSQL database. Finally, run the development server locally on your system.
```bash
$ python manage.py collectstatic --noinput
$ python manage.py migrate
... (OK)
$ python manage.py runserver
```
Open your browswer and head over to [http://localhost:8000](http://localhost:8000). If you can see "Hello How are you?", then you have successfully served ToDoApp on your system. Head over to the [Django Admin Dashboard](http://localhost:8000/admin), enter your login credentials and start using the Admin site.

## Docker Configuration

Docker is properly configured for this project, except for two files that require executable permissions on your system. You have different ways to do this based on your operating system. If you are using Ubuntu or MacOS, simply go to the /app folder and enter the following commands.
```bash
$ chmod +x entrypoint.sh
$ chmod +x entrypoint.prod.sh
```

If you are using Windows, open the Windows Explore window and locate these two files on the project folder. Right-click on a file, click on "properties" to open the property window, click on "Security" tab and make sure "Read & execute" is allowed for the current user. Click "Edit" to modify the permission to "Read & execute". After all, the point of this operation is to give executable permissions to these two files.

### Before we proceed to Docker containers, you need to turn off the development server otherwise they will conflict each other. Go to /app folder and quit the server with CTRL+C.

## Docker Development Container

Build development container images by entering the commands
```bash
$ docker-compose up -d --build
```
Wait for docker to finish building images. Once it is finished, you need to build container database, collect frontend static files for Djang to render and create a superuser to use the admin site.
```bash
$ docker-compose exec web python manage.py flush --noinput
$ docker-compose exec web python manage.py migrate --noinput
$ docker-compose exec web python manage.py collectstatic --noinput
$ docker-compose exec web python manage.py createsuperuser
```
Now head over to head over to [http://localhost:8000](http://localhost:8000) as before and see "Hello How are you?" on the page. Login the admin site with your credentials. You can bring down the containers with the following commands. ### Do not bring it down yet, as we will use the development container for Test Scripts.
```bash
$ docker-compose down -v
```

## Docker Production Container

The production container uses Nginx acting as a reverse-proxy for public access to the project, and port 8000 is only exposed internally, to other Docker services. The port will no longer be published to the host machine. Nginx is properly configured in this repository, and the app will be running at http://localhost:1337 after spinning up the production container images. You can build the production container images by entering the commands.
```bash
$ docker-compose -f docker-compose.prod.yml up -d --build
... done
$ docker-compose -f docker-compose.prod.yml exec web python manage.py flush --noinput
$ docker-compose -f docker-compose.prod.yml exec web python manage.py migrate --noinput
$ docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --noinput
$ docker-compose -f docker-compose.prod.yml exec web python manage.py createsuperuser
```
Head over to [http://localhost:1337](http://localhost:1337) (not 8000) and see "Hello How are you?" on the main page. Sign in the admin site with your credentials. You can build the production container images by entering the commands.
```bash
$ docker-compose -f docker-compose.prod.yml down -v
```
### Do not bring it down yet, as we will use the production container for Test Scripts.

## Test Scripts

The production server is running on [http://localhost:1337](http://localhost:1337). The ToDoApp provides REST API endpoints to handle the following operations.
1. Add a ToDo.
2. Delete a ToDo.
3. Update a ToDo.
4. List all ToDos.
  a. Filter ToDos by one or more fields.

We will run the test scripts on a Python intepreter. To enter the interpreter, we give the following command
```bash
$ docker-compose exec web python manage.py shell
...
>>> 
```
There is a list of testing tools/API's to use, and we will use the RequestsClient from the [Django REST framework](https://www.django-rest-framework.org/api-guide/testing/). Before we add a ToDo item, we will create a user who will possess an API Key. Only via API Key can a user perform the following actions.

1. Create a user
```python
>>> from rest_framework.test import RequestsClient
>>> client = RequestsClient()
>>> user_data = {
>>>     'username': 'hello_todoapp',
>>>     'password': 'hello_todoapp',
>>>     'first_name': 'hello',
>>>     'last_name': 'todoapp',
>>>     'email': 'hello@todoapp.com',
>>> }
>>> response = client.post('http://localhost:8000/todoapp/api/createuser/', user_data)
>>> response.content
b'{"api_key":"zwjV4rVN.oaroZ7uak5MFMju8BbPgXL3uM0LuAf9Z"}'
```

2. Retreive API Key

In case users forgets their API Key, they can retreive this key using their usernames and passwords.
```python
>>> credentials = {
>>>      'username': 'hello_todoapp',
>>>      'password': 'hello_todoapp'
>>> }
>>> response = client.post('http://localhost:8000/todoapp/api/getapikey/', credentials)
>>> response.content
b'{"api_key":"zwjV4rVN.oaroZ7uak5MFMju8BbPgXL3uM0LuAf9Z"}'
```

3. Add a Todo item

Assign the API Key to a variable and use it from now on.
```python
>>> api_key = "zwjV4rVN.oaroZ7uak5MFMju8BbPgXL3uM0LuAf9Z"
>>> todo_data = {
>>>     'task_title': 'Do this task',
>>>     'task_description': 'Do it now',
>>>     'task_state': '1',
>>>     'task_due_date': '2020-02-20',
>>> }
>>> response = client.post('http://localhost:8000/todoapp/api/create/', todo_data, headers={'Authorization': 'Api-Key %s' % api_key })
>>> response.content
b'{"message":"This item is created."}'
```
We can check if this item is created from the [admin site](http://localhost:1337/admin/todo_app/todoapp/). Let's add another Todo item.
```python
>>> api_key = "zwjV4rVN.oaroZ7uak5MFMju8BbPgXL3uM0LuAf9Z"
>>> todo_data = {
>>>     'task_title': 'Do that task',
>>>     'task_description': 'Do it later',
>>>     'task_state': '2',
>>>     'task_due_date': '2020-02-21',
>>> }
>>> response = client.post('http://localhost:8000/todoapp/api/create/', todo_data, headers={'Authorization': 'Api-Key %s' % api_key })
>>> response.content
b'{"message":"This item is created."}'
```

4. List all ToDos

A user can only see his/her ToDo items via their API keys.
```python
>>> response = client.get('http://localhost:8000/todoapp/api/list/', headers={'Authorization': 'Api-Key %s' % api_key })
>>> response.content
b'[{"task_id":1,"task_title":"Do this task","task_description":"Do it now","task_state":"1","task_due_date":"2020-02-20","user_id":2},{"task_id":2,"task_title":"Do that task","task_description":"Do it later","task_state":"2","task_due_date":"2021-02-20","user_id":2}]'
```
There is an API built for retreiving a list of options for sorting and filtering. This is list of data is great for frontend developers to make select and option user endpoints.
```python
>>> response = client.post('http://localhost:8000/todoapp/api/options/', headers={'Authorization': 'Api-Key %s' % api_key })
>>> response.content
b'{"sort_by":["task_id","task_title","task_description","task_state","task_due_date"],"filter_title_by":["Do that task","Do this task"],"filter_description_by":["Do it later","Do it now"],"filter_state_by":[["1","Todo"],["2","In Progress"],["3","Done"]],"filter_due_date_by":["2020-02-20","2021-02-20"],"reverse_order":[true,false]}'
```
Now we can see clearly what to enter for sorting and filtering, and we can use the following example.
```python
>>> option_data = {
>>>     "sort_by": 'task_title',
>>>     "filter_title_by": '',
>>>     "filter_description_by": '',
>>>     "filter_state_by": '',
>>>     "filter_due_date_by": '',
>>>     "reverse_order": True,
>>> }
>>> response = client.post('http://localhost:8000/todoapp/api/list/', option_data, headers={'Authorization': 'Api-Key %s' % api_key })
>>> response.content
b'[{"task_id":1,"task_title":"Do this task","task_description":"Do it now","task_state":"1","task_due_date":"2020-02-20","user_id":2},{"task_id":2,"task_title":"Do that task","task_description":"Do it later","task_state":"2","task_due_date":"2021-02-20","user_id":2}]'
>>> option_data = {
>>>     "sort_by": 'task_id',
>>>     "filter_title_by": 'Do it now',
>>>     "filter_description_by": '',
>>>     "filter_state_by": '',
>>>     "filter_due_date_by": '',
>>>     "reverse_order": True,
>>> }
>>> response = client.post('http://localhost:8000/todoapp/api/list/', option_data, headers={'Authorization': 'Api-Key %s' % api_key })
>>> response.content
b'[]'
```
We get an empty list because 'Do it now' is entered in 'filter_title_by', which is a mismatch. In practice, the frontend developers will fetch the options list and make select list for users. 

5. Update a ToDo

Let's move on to updating and deleting a Todo item. For both actions, we need to know the ID of the ToDo item. If the ID and the user API Key match, we can perform the actions.
```python
>>> todo_id = 1
>>> todo_data = {
>>>     "task_title": 'Go to work',
>>>     "task_description": 'Work related item',
>>>     "task_state": '3',
>>>     "task_due_date": '2021-02-17',
>>> }
>>> response = client.put('http://localhost:8000/todoapp/api/update/%s/' % todo_id, todo_data, headers={'Authorization': 'Api-Key %s' % api_key })
>>> response.content
b'{"message":"Item is updated"}'
```

6. Delete a ToDo item.

To delete an item, all we need to know is the ID of the item.
```python
>>> todo_id = 1
>>> response = client.delete('http://localhost:8000/todoapp/api/delete/%s/' % todo_id, headers={'Authorization': 'Api-Key %s' % api_key })
>>> response.content
b'{"message":"Item is deleted"}'
```

7. Quit from Shell

Remember to quit your work and bring down containers after you are finished experimenting the testing scripts.
```python
>>> quit()
```
```bash
$ docker-compose -f docker-compose.prod.yml down -v
```

## Conclusion

The ToDoApp is a server app that uses programming techniques from Django, PostgreSQL and Docker. Django is responsible for maintaining the integrity of the coding part in a MVC framework. PostgreSQL is used to manage the database, while Docker hosts the program in a static server setting. The TodoApp allows users create new user and retreive api keys, as well as creating, updating, deleting, listing, sorting and filtering ToDo items on the server side. The ReactJS frontend is properly configured and ready to use, and with a little bit of effort, one can make a beautiful frontend ToDo app with the said features for public users.
