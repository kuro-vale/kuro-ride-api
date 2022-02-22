# Django
from django.urls import path
# Ride views
from rides import views

urlpatterns = [
    path('<str:slug_name>/create/', views.create_ride, name='create_ride'),
    path('<str:slug_name>/', views.get_rides, name='get_rides'),
    path('<str:ride_id>/update/', views.update_ride, name='update_ride'),
]
