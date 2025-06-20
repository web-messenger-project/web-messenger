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
    
    except chatDB.DoesNotExist:
        return Response({'Błąd': 'Taki login nie istnieje'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@check_api_key
def createChat(request):
    """Create private or group chat"""

    content = json.loads(request.data["_content"])

    try:
        for param in ('name', 'members', 'is_gropu_chat'):
            if content.get(param) is None:
                raise KeyError()

        serializer = chatDBSerializer(data=content)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({'Błąd': 'Nie ma wszystkich pól, jest ich za dużo lub są w nieprawidłowym formacie'}, status=status.HTTP_400_BAD_REQUEST)

    except KeyError:
        return Response({'Błąd': 'Nie ma wszystkich parametrów (lub jest za dużo)'}, status=status.HTTP_400_BAD_REQUEST)
    
    except TypeError:
        return Response({'Błąd': 'Body nie jest w formacie JSON'}, status=status.HTTP_400_BAD_REQUEST)

    except ValueError:
        return Response({'Błąd': 'Format jednego z pól jest nieprawidłowy'}, status=status.HTTP_400_BAD_REQUEST)

    except DatabaseError:
        return Response({'Błąd': 'Baza danych nie działa :('}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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