from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView
import todo_app.urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('todoapp/', include(todo_app.urls)),

    re_path(r'^.*', TemplateView.as_view(template_name='index.html')),
]
