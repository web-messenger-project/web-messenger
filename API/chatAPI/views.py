from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db import DatabaseError
from rest_framework import status
from datetime import datetime

from db.models import chatDB, userDB
from .serializers import chatDBSerializer, chatDBMessagesSerializer
from userAPI.serializers import userDBSerializer

from userAPI.views import check_api_key, contain_necessary_fields
import json


# chat administartion operations

@api_view(['POST'])
@check_api_key
def getMessages(request):
    """Get messages to load chat's history"""

    content = json.loads(request.data["_content"]) # parametry podane przez klienta

    try:
        chat_id = content.get('id') # wez ID

        if chat_id is None: # czy id istnieje
            return Response({'Błąd': 'Nie podano ID chatu'}, status=status.HTTP_400_BAD_REQUEST)

        response = chatDB.objects.filter(id=chat_id).first().messages # weź istniejace wiadomości tego chatu
        serializer = chatDBMessagesSerializer(response) # serializuj je
    
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
    
    else:
        return Response(serializer.data, status=status.HTTP_200_OK) # zwroc

@api_view(['POST'])
@check_api_key
def createChat(request):
    """Create private or group chat"""

    content = json.loads(request.data["_content"]) # parametry body requesta

    try:
        if not contain_necessary_fields(content, ('name', 'members', 'is_gropu_chat')): # czy w parametrach sa te pola
            raise KeyError()

        serializer = chatDBSerializer(data=content) # serializuj body requesta, KTORE JEST PODSAWĄ STWORZENIA CHATU
        # zwiera uzytkownikow (members), nazwe i czy jest group chatem czy nie

        if serializer.is_valid(): # jesli mozna stworzyc
            serializer.save() # do zapisuje sie chat

            for member in content.get('members'): # przypisuje uzytkownikom w 'included_in_these_chats' ID chatu, do ktorego zostali dodanie
                user_login = member.get('login') # znajduje login kazdego uzytkownika z parametru members
                user_record = userDB.objects.filter(login=user_login).first() # znajduje go w bazie danych

                if user_record is not None: # jesli jest, to dodaje do listy ID jego chatow nowy chat
                    user_record.included_in_these_chats.append(content.get('id'))
                    user_record.save()
                else:
                    return Response({'Błąd': 'Takiego użytkownika nie ma'}, status=status.HTTP_404_NOT_FOUND)

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

@api_view(['POST'])
@check_api_key
def addUserToChat(request):
    """Adds user to chat on provided ID"""

    content = json.loads(request.data["_content"]) # wez parametry

    try:
        if not contain_necessary_fields(content, ('chatID', 'login')): # czy sa te parametry
            raise KeyError()

        chat = chatDB.objects.filter(id=content.get('chatID')).first() # znajdz w bazie danych chat z parametru
        user = userDB.objects.filter(login=content.get('login')).first() # i uzytkowanika

        if chat is None or user is None: # gdy nie ma obu do zakoncz
            return Response({'Błąd': 'Nie znaleziono podanego użytkownika lub chatu'}, status=status.HTTP_404_NOT_FOUND)

        chat.members.append({'name': user.name, 'surname': user.surname, 'login': user.login}) # do czlonok czatu zostaje dodany uzytkownik ze wszystkimi parametrami
        chat.save()

        user.included_in_these_chats.append({'id': chat.id})
        user.save()

        serializer = userDBSerializer(user)

    except KeyError:
        return Response({'Błąd': 'Nie ma wszystkich parametrów (lub jest za dużo)'}, status=status.HTTP_400_BAD_REQUEST)
    
    except TypeError:
        return Response({'Błąd': 'Body nie jest w formacie JSON'}, status=status.HTTP_400_BAD_REQUEST)

    except ValueError:
        return Response({'Błąd': 'Format jednego z pól jest nieprawidłowy'}, status=status.HTTP_400_BAD_REQUEST)

    except DatabaseError:
        return Response({'Błąd': 'Baza danych nie działa :('}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    else:
        return Response({serializer.data}, status=status.HTTP_200_OK)

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


# messages operations

@api_view(['POST'])
@check_api_key
def postMessage(requset):
    pass