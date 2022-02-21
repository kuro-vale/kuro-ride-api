# Django
from django.urls import path
# Ride views
from rides import views

urlpatterns = [
    path('<str:slug_name>/create/', views.create_ride, name='create_ride'),
]
