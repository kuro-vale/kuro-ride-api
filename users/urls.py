# Django
from django.urls import path
# Circle views
from users import views

urlpatterns = [
    path('login/', views.UserLoginAPIView.as_view(), name='login'),
    path('signup/', views.SignUpAPIView.as_view(), name='signup')
]
