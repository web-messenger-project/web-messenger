from django.urls import path
from userAPI import views

urlpatterns = [
    path('api/login/', views.login, name='login'),
    path('api/register/', views.register, name='register'),
    path('api/delete/', views.delete_user, name='delete_user'),
    path('api/getall/', views.getAllUsers, name='getall')
]