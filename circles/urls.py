# Django
from django.urls import path
# Circle views
from circles import views

urlpatterns = [
    path('circles/', views.list_circles),
    path('circles/create/', views.create_circle)
]
