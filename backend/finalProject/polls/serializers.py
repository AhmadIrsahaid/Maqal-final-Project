from rest_framework import serializers, permissions

from polls.models import *

from backend.finalProject.polls.models import User, Category, Comments, Article, Tag


class ReaderSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class ArticleSerializer(serializers.ModelSerializer):
    authors = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all().filter(is_author=True))
    class Meta:
        model = Article
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class BookMarksSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookMarks
        fields = '__all__'

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
            model = Likes
            fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = '__all__'

class TagSerializer(serializers.ModelSerializer):
    articles = serializers.PrimaryKeyRelatedField(many=True, queryset=Article.objects.all())
    class Meta:
        model = Tag
        fields = '__all__'