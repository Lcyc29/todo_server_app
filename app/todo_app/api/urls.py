from django.urls import path
from django.conf.urls import url
# OrderMethod, Company, ChargeAccount
from .views import (
    CreateUserView,
    RetrieveAPIView,
    TodoCreateView,
    TodoUpdateView,
    TodoDeleteView,
    TodoOptionsView,
    TodoListView,
)

urlpatterns = [
    path('createuser/', CreateUserView.as_view()),
    path('getapikey/', RetrieveAPIView.as_view()),
    path('create/', TodoCreateView.as_view()),
    path('update/<pk>/', TodoUpdateView.as_view()),
    path('delete/<pk>/', TodoDeleteView.as_view()),
    path('options/', TodoOptionsView.as_view()),
    path('list/', TodoListView.as_view()),
]
