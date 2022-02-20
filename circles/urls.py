# Django
from django.urls import path
# Circle views
from circles import views

urlpatterns = [
    path('circles/', views.list_circles, name='list_circles'),
    path('circle/<str:slug_name>/', views.get_circle, name='get_circle'),
    path('circles/create/', views.create_circle, name='create_circle'),
    path('circles/<str:slug_name>/update/', views.update_circle, name='update_circle'),
    path('circles/<str:slug_name>/delete/', views.delete_circle, name='delete_circle'),
    path('circle/<str:slug_name>/members/', views.get_circle_members, name='get_circle_members'),
    path('circle/<str:slug_name>/<str:username>/', views.get_circle_member, name='get_circle_member'),
    path('circle/<str:slug_name>/<str:username>/kick/', views.kick_circle_member, name='kick_circle_member'),
]
