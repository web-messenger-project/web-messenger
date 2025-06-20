from django.urls import path
from chatAPI import views

urlpatterns = [
    path('api/get/', views.getMessages, name='get'),
]