# views.py
from django.contrib.auth.forms import UserCreationForm
from django.http import JsonResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from polls.models import Article, User
from django.urls import reverse_lazy
from polls.form import *
from django.views.generic import TemplateView
from .models import Article
from django.contrib.auth import authenticate, login
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .form import ReaderCreationForm
def home(request):
    data = {
        'message': 'Welcome from Django!',
        'content': 'This data comes from your Django backend',
    }
    return JsonResponse(data)


class BasePageView(TemplateView):
    template_name = "base.html"
    context_object_name = "base"


class AboutPageView(TemplateView):
    template_name = "About.html"



class HomePageView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["articles"] = Article.objects.all()
        return ctx

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

# Reader views
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



class ReaderSignUpView(CreateView):
    form_class = ReaderSignUpForm
    success_url = reverse_lazy("home-page")
    template_name = "registration/signup.html"

    def form_valid(self, form):
        form.save()
        auth_user = authenticate(self.request, email=User.email, password=form.cleaned_data["password1"])
        if auth_user:
            login(self.request, auth_user)
        return super().form_valid(form)