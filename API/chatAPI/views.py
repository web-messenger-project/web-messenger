from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db import DatabaseError
from rest_framework import status

from db.models import chatDB, userDB
from .serializers import chatDBSerializer, chatDBMessagesSerializer

from userAPI.views import check_api_key
import json

@api_view(['POST'])
@check_api_key
def getMessages(request):
    """Get messages to load chat's history"""

    content = json.loads(request.data["_content"])

    try:
        chat_id = content.get('id')

        if chat_id is None:
            return Response({'Błąd': 'Nie podano ID chatu'}, status=status.HTTP_400_BAD_REQUEST)

        response = chatDB.objects.filter(id=chat_id).first().messages
        serializer = chatDBMessagesSerializer(response)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    except KeyError:
        return Response({'Błąd': 'Nie ma wszystkich parametrów (lub jest za dużo)'}, status=status.HTTP_400_BAD_REQUEST)
    
    except TypeError:
        return Response({'Błąd': 'Body nie jest w formacie JSON'}, status=status.HTTP_400_BAD_REQUEST)

    except ValueError:
        return Response({'Błąd': 'Format jednego z pól jest nieprawidłowy'}, status=status.HTTP_400_BAD_REQUEST)

    except DatabaseError:
        return Response({'Błąd': 'Baza danych nie działa :('}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@check_api_key
def createChat(request):
    pass

@api_view(['PATCH'])
@check_api_key
def addUserToChat(request):
    pass

@api_view(['DELETE'])
@check_api_key
def deleteChat(request):
    pass

@api_view(['PATCH'])
@check_api_key
def updateChatMetaData(request):
    pass

@api_view(['PATCH'])
@check_api_key
def deleteUserFromChat(requset):
    pass