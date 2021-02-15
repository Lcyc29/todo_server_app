from django.urls import path
from django.conf.urls import url
# OrderMethod, Company, ChargeAccount
from .views import (
     TodoCreateView,
     TodoUpdateView,
)

urlpatterns = [
    path('create/', TodoCreateView.as_view()),
    path('update/<key>/', TodoUpdateView.as_view()),
]
