# polls/urls.py
from django.urls import path
from . import views
from .views import ArticleCreateView, ArticleListView

urlpatterns = [
    path('api/home/', views.home, name='home'),
    path('api/card/' , views.list_articles , name='list_articles'),
    path('create/', ArticleCreateView.as_view() , name='create-article'),
    path('list/', ArticleListView.as_view() , name='list-articles'),
    path('edit/<int:pk>/', views.ArticleUpdateView.as_view() , name='edit-article'),
    path('article/<int:pk>/', views.ArticleDetailView.as_view() , name='article-detail'),
    path('delete/<int:pk>/', views.ArticleDeleteView.as_view() , name='article-delete'),
]
