from django.urls import path
from chatAPI import views

urlpatterns = [
    path('api/get/', views.getMessages, name='get'),
    path('api/create/', views.createChat, name='create'),
    path('api/addToChat/', views.addUserToChat, name='addToChat'),
    path('api/deleteChat/', views.deleteChat, name='delete'),
    path('api/updateChatData/', views.updateChatMetaData, name='updateChatData'),
    path('api/deleteUser/', views.deleteUserFromChat, name='deleteUser'),
]