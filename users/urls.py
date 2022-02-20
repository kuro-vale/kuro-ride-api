# Django
from django.urls import path
# Views
from users import views

urlpatterns = [
    path('login/', views.UserLoginAPIView.as_view(), name='login'),
    path('signup/', views.SignUpAPIView.as_view(), name='signup'),
    path('verify/', views.AccountVerificationAPIView.as_view(), name='verify'),
    path('logout/', views.logout, name='logout'),
    path('update/', views.update_user, name='update_user'),
    path('delete/', views.delete_user, name='delete_user'),
    path('profile/<str:username>/', views.get_user, name='get_user'),
    path('profile/', views.update_profile, name='update_profile'),
]
