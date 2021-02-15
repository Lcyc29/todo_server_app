from django.conf.urls import url, include, re_path
from django.urls import path

urlpatterns = [
    path('api/', include('todo_app.api.urls')),
]