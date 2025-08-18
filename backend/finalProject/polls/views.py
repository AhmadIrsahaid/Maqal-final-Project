# views.py
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.db.models import Q
from .models import Article, User, Comments
from polls.form import ReaderCreationForm, ReaderSignUpForm ,AddComment


def home(request):
    return JsonResponse({
        'message': 'Welcome from Django!',
        'content': 'This data comes from your Django backend',
    })


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
    data = [
        {"title": a.title, "content": a.content}
        for a in Article.objects.all()
    ]
    return JsonResponse(data, safe=False)


class ArticleListView(ListView):
    model = Article
    context_object_name = "articles"
    template_name = "articles/article_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        can_create = (
                user.is_authenticated and getattr(user, "role", "") in ("admin", "author")
        )
        context["can_create_article"] = can_create
        return context
class ArticleCreateView(CreateView):
    model = Article
    fields = "__all__"
    template_name = "articles/article_create.html"
    context_object_name = "article"
    success_url = reverse_lazy("list-articles")

    def test_func(self):
        return self.request.user.has_perm("auth.add_article")


class ArticleUpdateView(UpdateView):
    model = Article
    fields = "__all__"
    template_name = "articles/article_update.html"
    context_object_name = "article"
    success_url = reverse_lazy("list-articles")

    def test_func(self):
        return self.request.user.has_perm("auth.change_article")


class ArticleDetailView(DetailView):
    model = Article
    template_name = "articles/article_detail.html"
    context_object_name = "articles"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['can_edit'] = self.object.can_edit(self.request.user)
        ctx['comment_form'] = AddComment()
        return ctx

    def get_success_url(self):
         return reverse('article-detail',kwargs={'pk' : self.object.pk})


    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = AddComment(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.article = self.object
            comment.save()
            return redirect(self.get_success_url())
        ctx = self.get_context_data()
        ctx['comment_form'] = form
        return self.render_to_response(ctx)




class ArticleDeleteView(DeleteView):
    model = Article
    template_name = "articles/article_delete.html"
    context_object_name = "article"
    success_url = reverse_lazy("list-articles")

    def test_func(self):
        return self.request.user.has_perm("auth.delete_article")


class UserListView(ListView):
    model = User
    template_name = "users/list_user.html"
    context_object_name = "users"


class UserCreateView(CreateView):
    model = User
    form_class = ReaderCreationForm
    template_name = "users/create_user.html"
    context_object_name = "user"
    success_url = reverse_lazy("user-list")
    def test_func(self):
        return self.request.user.has_perm("auth.add_user")

class UserDetailView(DetailView):
    model = User
    template_name = "users/detail_user.html"
    context_object_name = "user"



class ReaderSignUpView(CreateView):
    form_class = ReaderSignUpForm
    success_url = reverse_lazy("home-page")
    template_name = "registration/signup.html"

    def form_valid(self, form):
        user = form.save()
        auth_user = authenticate(self.request,
                                 email=form.cleaned_data.get("email"),
                                 password=form.cleaned_data.get("password1"))
        if auth_user:
            login(self.request, auth_user)
        return super().form_valid(form)


class CommentCreateView(CreateView):
        model = Comments
        form_class = AddComment
        template_name = "articles/article_detail.html"
        context_object_name = "comment"

        def form_valid(self, form):
            form.instance.user = self.request.user
            form.instance.article_id = self.kwargs["pk"]
            return super().form_valid(form)

        def get_success_url(self):
            return reverse("article-detail", args=[self.kwargs["pk"]])


class SearchResultsView(ListView):
    model = Article
    context_object_name = "articles"
    template_name = "articles/article_list.html"


    def get_queryset(self):
        query = self.request.GET.get("q")
        return Article.objects.filter(
            Q(title__icontains=query) |
            Q(publication_date__icontains=query)
        )