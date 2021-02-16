from django.urls import path
from django.conf.urls import url
# OrderMethod, Company, ChargeAccount
from .views import (
     TodoCreateView,
     TodoUpdateView,
     TodoDeleteView,
     TodoListView,
)

urlpatterns = [
    path('create/', TodoCreateView.as_view()),
    path('update/<key>/', TodoUpdateView.as_view()),
    path('delete/<key>/', TodoDeleteView.as_view()),
    path('list/', TodoListView.as_view()),
]
