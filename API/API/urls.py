from django.urls import path, include

urlpatterns = [
    path('user/', include('userLoggingAPI.urls')),
    path('chat/', include('chatLoadingAPI.urls')),
]