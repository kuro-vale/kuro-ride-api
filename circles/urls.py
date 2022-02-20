# Django
from django.urls import path
# Circle views
from circles import views

urlpatterns = [
    path('circles/', views.list_circles, name='list_circles'),
    path('circles/<str:slug_name>/', views.get_circle, name='get_circle'),
    path('circles/create/', views.create_circle, name='create_circle'),
    path('circles/<str:slug_name>/update/', views.update_circle, name='update_circle'),
    path('circles/<str:slug_name>/delete/', views.delete_circle, name='delete_circle'),
]
