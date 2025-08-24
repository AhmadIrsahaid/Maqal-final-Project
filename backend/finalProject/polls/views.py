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
from django.db.models import Q, Count
from .models import Article, User, Comments, Likes, BookMarks, Category
from polls.form import ReaderCreationForm, ReaderSignUpForm, AddComment, LikeForm, BookmarkForm
from django.views import View
from django.contrib import messages
from typing import List
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
        article = self.object
        user = self.request.user

        # Define forms
        ctx["comment_form"] = AddComment()
        ctx["like_form"] = LikeForm()
        ctx["bookmarks_form"] = BookmarkForm()

        # count the number of likes and bookMark
        ctx["likes_count"] = article.article_likes.count()
        ctx["bookmarks_count"] = article.bookmarks.count()

        #chnage the status if like and bookmark
        ctx["user_has_liked"] = user.is_authenticated and article.article_likes.filter(reader=user).exists()
        ctx["user_has_bookMark"] = user.is_authenticated and article.bookmarks.filter(reader=user).exists()

        ctx["comments"] = article.comments.select_related("reader").order_by("-date_of_comment")

        ctx["can_edit"] = getattr(article, "can_edit", lambda u: False)(user)
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
    # target_date =

    def get_queryset(self):
        query = self.request.GET.get("q")
        return Article.objects.filter(
            Q(title__icontains=query)
            # | Q(Article.objects.filter(publication_date=target_date))
        )

class LikeToggleView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        article = Article.objects.get(pk=self.kwargs["pk"])
        like, created = Likes.objects.get_or_create(article=article, reader=request.user)
        if created:
            messages.success(request, "Liked.")
        else:
            like.delete()
            messages.info(request, "Like removed.")
        return redirect("article-detail", pk=article.pk)


class Bookmarks(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        article = Article.objects.get(pk=self.kwargs["pk"])
        bookmark , create = BookMarks.objects.get_or_create(article=article , reader=request.user)
        if create:
            messages.success(request, "Bookmark created.")
        else:
            bookmark.delete()
            messages.info(request, "Bookmark removed.")
        return redirect("article-detail", pk=article.pk)



class AuthorListView(ListView):
    model = User
    context_object_name = "users"
    template_name = "Authors/AuthorList.html"

class AllBookMarkView(ListView):
    model = Article
    template_name = "articles/allBookMarks.html"
    context_object_name = "articles"

    def get_queryset(self):
        return Article.objects.filter(bookmarks__reader=self.request.user)


class AllCategoriesView(ListView):
    model = Category
    context_object_name = "categories"
    template_name = "articles/AllCategoriesList.html"


    def get_context_data(self, **kwargs):

        ctx = super().get_context_data(**kwargs)
        category_article_count = {}
        all_categories = Category.objects.all()
        for cat in all_categories:
            category_article_count[cat.id] = cat.number_of_article()
        ctx["category_article_count"] = category_article_count
        return ctx


class ArticleAndCategoryListView(ListView):

    model = Article
    context_object_name = "articles"
    template_name = "articles/article_list.html"

    def get_queryset(self):
       articles = Article.objects.all()
       cat_id = Category.objects.get(pk=self.kwargs["pk"])
       obj =  articles.filter(category=cat_id)
       return obj

