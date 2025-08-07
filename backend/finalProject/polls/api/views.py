from rest_framework.generics import*

from backend.finalProject.polls.models import Article
from backend.finalProject.polls.serializers import ArticleSerializer


class ArticleListAPIView(ListAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
