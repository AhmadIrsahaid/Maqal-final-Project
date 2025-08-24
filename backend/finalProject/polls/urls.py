# polls/urls.py
from django.urls import path ,include
from . import views
from polls.views import *
from django.views.generic import TemplateView

from .form import BookmarkForm

urlpatterns = [
    path("accounts/", include("django.contrib.auth.urls")),
    # path("", TemplateView.as_view(template_name="home.html"), name="home"),
    path('api/home/', views.home, name='home'),
    path('api/card/' , views.list_articles , name='list_articles'),
    path('article/create/', ArticleCreateView.as_view() , name='create-article'),
    path('article/list/', ArticleListView.as_view() , name='list-articles'),
    path('article/edit/<int:pk>/', views.ArticleUpdateView.as_view() , name='edit-article'),
    path('article/detail/<int:pk>/', views.ArticleDetailView.as_view() , name='article-detail'),
    path('article/delete/<int:pk>/', views.ArticleDeleteView.as_view() , name='article-delete'),
    path('user/list/', views.UserListView.as_view() , name='user-list'),
    path('user/create/', UserCreateView.as_view() , name='user-create'),
    path('user/detail/<int:pk>/', UserDetailView.as_view() , name='user-detail'),
    path('', views.HomePageView.as_view(), name='home-page'),
    # path('', views.BasePageView.as_view(), name='base-page'),
    path('about/', views.AboutPageView.as_view(), name='about-page'),
    path("signup/", ReaderSignUpView.as_view(), name="signup"),
    path("article/<int:pk>/comment/", CommentCreateView.as_view(), name="article-add-comment"),
    path("search/", SearchResultsView.as_view(), name="search_results"),
    path("likes/<int:pk>",LikeToggleView.as_view(),name="add-like"),
    path("authors/list",AuthorListView.as_view(),name="author-list"),
    path("article/<int:pk>/bookmark",Bookmarks.as_view(),name="add-bookmark"),
    path("article/bookmarks/<int:pk>" , AllBookMarkView.as_view() , name="all-bookmark"),
    path("article/categories/", AllCategoriesView.as_view() , name="all-categories"),
    path("article/categories/<int:pk>", ArticleAndCategoryListView.as_view() , name="all-categories-with-article"),

]
