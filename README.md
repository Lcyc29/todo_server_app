# ToDoApp with Django PostgreSQL Docker and Nginx

For this project, we have three primary tasks. First, we will create a TODO server app with Python, Django, and PostgreSQL. The primary interface is
a REST API, and we will provide an admin dashboard using Django’s Admin Site system for backend management. Next, we will configure the app to run on a Gunicorn WSGI server, behind an NGINX instance acting as a reverse-proxy. All components — Django/Gunicorn, Postgres, NGINX — will be deployed as Docker containers via docker-compose comands (i.e, docker-compose up should bring up the entire system and docker-compose down to shut everything down). Finally, we will provide Python script to test ToDoApp's REST API as a normal user. 

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
|
│   .env.dev
│   .env.prod
│   .env.prod.db
│   .gitignore
│   docker-compose.prod.yml
│   docker-compose.yml
│   README.md
│
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
│   │
│   ├───.vscode
│   │       
│   ├───frontend
│   │
│   ├───todo_app
│   │
│   └───todo_server_app
│
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
If you are using Windows, open the Windows Explore window and locate these two files on the project folder. Right-click on a file, click on "properties" to open the property window, click on "Security" tab and make sure "Read & execute" is allowed for the current user. Click "Edit" to modify the permission to "Read & execute". After all, the point of this operation is to give executable permissions to these two files. Feel free to 







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