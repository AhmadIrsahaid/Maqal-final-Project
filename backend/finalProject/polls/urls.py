# polls/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('api/home/', views.home, name='home'),
    path('api/titile/' , views.list_articles , name='list_articles'),
]
