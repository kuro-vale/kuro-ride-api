# Django
from django.urls import path
# Circle views
from circles import views

urlpatterns = [
    path('', views.list_circles, name='list_circles'),
    path('<str:slug_name>/circle/', views.get_circle, name='get_circle'),
    path('create/', views.create_circle, name='create_circle'),
    path('<str:slug_name>/update/', views.update_circle, name='update_circle'),
    path('<str:slug_name>/delete/', views.delete_circle, name='delete_circle'),
    path('<str:slug_name>/members/', views.get_circle_members, name='get_circle_members'),
    path('<str:slug_name>/members/<str:username>/', views.get_circle_member, name='get_circle_member'),
    path('<str:slug_name>/members/<str:username>/kick/', views.kick_circle_member, name='kick_circle_member'),
    path('invitations/<str:slug_name>/', views.get_invitations, name='get_invitations'),
    path('invitations/<str:slug_name>/create/', views.create_invitation, name='create_invitation'),
    path('invitations/<str:slug_name>/join/', views.join_circle, name='join_circle')
]
