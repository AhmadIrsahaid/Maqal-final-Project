# views.py
from django.contrib.auth.forms import UserCreationForm
from django.http import JsonResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from polls.models import Article, User
from django.urls import reverse_lazy
from polls.form import *

def home(request):
    data = {
        'message': 'Welcome from Django!',
        'content': 'This data comes from your Django backend',
    }
    return JsonResponse(data)



def list_articles(request):
    articles = Article.objects.all()
    data = [
        {

            'title': article.title,
            'content' : article.content

        }
        for article in articles
    ]
    return JsonResponse(data, safe=False)



# article views
class ArticleListView(ListView):
    model = Article
    context_object_name = "articles"
    template_name = "articles/article_list.html"

class ArticleCreateView(CreateView):
    model = Article
    fields = "__all__"
    template_name = "articles/article_create.html"
    context_object_name = "articles"
    success_url = reverse_lazy("list-articles")

class ArticleUpdateView(UpdateView):
    model = Article
    fields = "__all__"
    template_name = "articles/article_update.html"
    context_object_name = "articles"
    success_url = reverse_lazy("list-articles")

class ArticleDetailView(DetailView):
    model = Article
    template_name = "articles/article_detail.html"
    context_object_name = "articles"

class ArticleDeleteView(DeleteView):
    model = Article
    template_name = "articles/article_delete.html"
    context_object_name = "articles"
    success_url = reverse_lazy("list-articles")

# Authors views
class UserListView(ListView):
    model = User
    template_name = "users/list_user.html"
    context_object_name = "users"


class UserCreateView(CreateView):
    model = User
    form_class = ReaderCreationForm
    template_name = "users/create_user.html"
    context_object_name = "users"
    success_url = reverse_lazy("user-list")


class UserDetailView(DetailView):
    model = User
    template_name = "users/detail_user.html"
    context_object_name = "users"
