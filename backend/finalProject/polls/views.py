# views.py
from django.http import JsonResponse

def home(request):
    data = {
        'message': 'Welcome from Django!',
        'content': 'This data comes from your Django backend',
        # Add any other data you want to send to React
    }
    return JsonResponse(data)