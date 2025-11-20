from django.shortcuts import render
from django.http import JsonResponse
from django.utils import timezone
import os

def home(request):
    """Home page with Docker info"""
    context = {
        'title': 'Django Docker Demo',
        'message': 'Welcome to Django running in Docker!',
        'database': os.environ.get('POSTGRES_DB', 'djangodb'),
        'host': os.environ.get('POSTGRES_HOST', 'db'),
        'current_time': timezone.now(),
    }
    return render(request, 'demo/home.html', context)

def api_info(request):
    """API endpoint with Docker info"""
    return JsonResponse({
        'status': 'success',
        'framework': 'Django',
        'database': os.environ.get('POSTGRES_DB', 'djangodb'),
        'database_host': os.environ.get('POSTGRES_HOST', 'db'),
        'debug': os.environ.get('DEBUG', '1'),
        'message': 'Django API is working!',
    })

