from django.urls import path
from userAPI import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('delete/', views.delete_user, name='delete_user'),
    path('getall/', views.getAllUsers, name='getall')
]