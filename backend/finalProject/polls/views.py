# views.py
from django.http import JsonResponse

from polls.models import Article


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
