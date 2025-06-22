from django.urls import path, include

urlpatterns = [
    path('user/', include('userAPI.urls')),
    path('chat/', include('chatAPI.urls')),
]