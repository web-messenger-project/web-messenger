from django.urls import path
from API import views

urlpatterns = [
    path('api/login/', views.login, name='login'),
    path('api/register/', views.register, name='register'),
    path('api/delete/', views.delete_user, name='delete_user'),
]