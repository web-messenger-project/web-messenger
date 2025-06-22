from django.urls import path
from chatAPI import viewsChat, viewsMessages

urlpatterns = [
    path('api/get/', viewsChat.getMessages, name='get'), # chat usage
    path('api/create/', viewsChat.createChat, name='create'),
    path('api/add/', viewsChat.addUserToChat, name='add'),
    path('api/deleteChat/', viewsChat.deleteChat, name='deleteChat'),
    path('api/update/', viewsChat.updateChatMetaData, name='update'),
    path('api/deleteUser/', viewsChat.deleteUserFromChat, name='deleteUser'),

    path('api/chatMeta/', viewsChat.getChatMeta, name='chatMeta'), # chat debug
    path('api/getall/', viewsChat.getAllChats, name='getall'),
    
    #path('api/post/', viewsMessages.postMessage, name='post'), # message usage
]