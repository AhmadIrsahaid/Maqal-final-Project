from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib import admin
from unicodedata import category

from .models import *


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    model = User
    list_display = ("email", "username", "first_name", "last_name", "role", "is_active", "is_staff")
    list_filter = ("role", "is_active", "is_staff", "is_superuser")
    search_fields = ("email", "username", "first_name", "last_name")
    ordering = ("email",)

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal Info", {"fields": ("username", "first_name", "last_name", "age", "birth_date", "profile_photo")}),
        ("Permissions", {"fields": ("role", "is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Important Dates", {"fields": ("last_login",)}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "username", "first_name", "last_name", "age", "birth_date", "profile_photo", "role",
                       "password1", "password2"),
        }),
    )

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ("last_login",)
        return self.readonly_fields

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "publication_date","get_author","get_category","content")
    readonly_fields = ('content_preview',)

    def get_author(self,obj):
        return " ,".join([author.username for author in obj.authors.all()])
    get_author.short_description = "Authors"

    def get_category(self, obj):
        return str(obj.category) if obj.category else "-"
    get_category.short_description = "Category"

    def content_preview(self, obj):
        return mark_safe(obj.content)

    content_preview.short_description = "Content"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (["type"])


class ReaderAdmin(admin.ModelAdmin):
    list_display = ("email", "username", "first_name", "last_name", "is_active")
    search_fields = ("email", "username", "first_name", "last_name")
    list_filter = ("is_active",)
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal Info", {"fields": ("username", "first_name", "last_name", "age", "birth_date", "profile_photo")}),
        ("Permissions", {"fields": ("is_active",)}),
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(role="reader")


class AuthorAdmin(admin.ModelAdmin):
    list_display = ("email", "username", "first_name", "last_name", "is_active")
    search_fields = ("email", "username", "first_name", "last_name")
    list_filter = ("is_active",)
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal Info", {"fields": ("username", "first_name", "last_name", "age", "birth_date", "profile_photo")}),
        ("Permissions", {"fields": ("is_active",)}),
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(role="author")

admin.site.register(ReaderProxy, ReaderAdmin)
admin.site.register(AuthorProxy, AuthorAdmin)

