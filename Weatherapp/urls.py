from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('weather/<str:city_name>/', views.weather_details, name='weather'),
]