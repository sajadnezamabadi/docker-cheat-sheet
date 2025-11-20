from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('api/', views.api_info, name='api_info'),
]

