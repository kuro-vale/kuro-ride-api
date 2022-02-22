# Django
from django.urls import path
# Ride views
from rides import views

urlpatterns = [
    path('<str:slug_name>/create/', views.create_ride, name='create_ride'),
    path('<str:slug_name>/', views.get_rides, name='get_rides'),
    path('<int:ride_id>/update/', views.update_ride, name='update_ride'),
    path('<str:slug_name>/<int:ride_id>/join/', views.join_ride, name='join_ride'),
    path('<int:ride_id>/end/', views.end_ride, name='end_ride'),
    path('<str:slug_name>/<int:ride_id>/rate/', views.rate_ride, name='rate_ride'),
]
