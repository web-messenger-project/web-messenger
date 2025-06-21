from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db import DatabaseError
from rest_framework import status
from datetime import datetime # message date and time

from db.models import chatDB, userDB
from .serializers import chatDBSerializer, chatDBMessagesSerializer, chatDBMembersSerializer
from userAPI.serializers import userDBSerializer

from userAPI.views import check_api_key, contain_necessary_fields


# chat administartion operations

@api_view(['POST'])
@check_api_key
def getMessages(request):
    """Gets messages to load chat's history"""

    try:
        chatID = request.content.get('id') # wez ID
        # request.content to parametry podane w body requesta

        if chatID is None: # czy id istnieje
            return Response({'Błąd': 'Nie podano ID chatu'}, status=status.HTTP_400_BAD_REQUEST)

        response = chatDB.objects.filter(id=chatID).first().messages # weź istniejace wiadomości tego chatu

        if response is not None:
            serializer = chatDBMessagesSerializer(response) # serializuj je
        else:
            return Response({'Błąd': 'Chat o takim ID nie istnieje'}, status=status.HTTP_404_NOT_FOUND)
    
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
    """Creates private or group chat"""

    try:
        if not contain_necessary_fields(request.content, ('name', 'members', 'is_group_chat')): # czy w parametrach sa te pola
            raise KeyError()

        serializer = chatDBSerializer(data=request.content) # serializuj body requesta, KTORE JEST PODSAWĄ STWORZENIA CHATU
        # zwiera uzytkownikow (members), nazwe i czy jest group chatem czy nie

        if serializer.is_valid(): # jesli mozna stworzyc
            serializer.save() # do zapisuje sie chat

            for member in request.content.get('members'): # przypisuje uzytkownikom w 'included_in_these_chats' ID chatu, do ktorego zostali dodanie
                user_login = member.get('login') # znajduje login kazdego uzytkownika z parametru members
                user_record = userDB.objects.filter(login=user_login).first() # znajduje go w bazie danych

                if user_record is not None: # jesli jest, to dodaje do listy ID jego chatow nowy chat
                    new_chat_id = serializer.instance.id

                    user_record.included_in_these_chats.append(new_chat_id)
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
    
    except userDB.DoesNotExist:
        return Response({'Błąd': 'Nie ma użytkownika z takim loginem'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@check_api_key
def addUserToChat(request):
    """Adds user to chat"""

    try:
        if not contain_necessary_fields(request.content, ('chatID', 'login')): # czy sa te parametry
            raise KeyError()

        chat = chatDB.objects.filter(id=request.content.get('chatID')).first() # znajdz w bazie danych chat z parametru
        user = userDB.objects.filter(login=request.content.get('login')).first() # i uzytkowanika

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
    
    except userDB.DoesNotExist:
        return Response({'Błąd': 'Nie ma użytkownika z takim loginem'}, status=status.HTTP_404_NOT_FOUND)
    
    except chatDB.DoesNotExist:
        return Response({'Błąd': 'Nie ma chatu o takim ID'}, status=status.HTTP_404_NOT_FOUND)
    
    else:
        return Response({serializer.data}, status=status.HTTP_200_OK)

@api_view(['DELETE'])
@check_api_key
def deleteChat(request):
    """Deletes chat on provided ID"""

    try:
        chatID = request.content.get('id')
        if chatID is None:
            return Response({'Błąd': 'Nie podano ID chatu'}, status=status.HTTP_400_BAD_REQUEST)

        chat = chatDB.objects.filter(id=chatID).first()
        copy = chat

        if chat is not None:
            chat.delete()
            serializer = chatDBSerializer(copy)
        else:
            return Response({'Błąd': 'Chat o takim ID nie istnieje'}, status=status.HTTP_404_NOT_FOUND)

    except TypeError:
        return Response({'Błąd': 'Body nie jest w formacie JSON'}, status=status.HTTP_400_BAD_REQUEST)
    
    except ValueError:
        return Response({'Błąd': 'Format jednego z pól jest nieprawidłowy'}, status=status.HTTP_400_BAD_REQUEST)
    
    except DatabaseError:
        return Response({'Błąd': 'Baza danych nie działa :('}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    except chatDB.DoesNotExist:
        return Response({'Błąd': 'Nie ma chatu o takim ID'}, status=status.HTTP_404_NOT_FOUND)
    
    else:
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)

@api_view(['PATCH'])
@check_api_key
def updateChatMetaData(request):
    """Updates chat name or other metadata
    atp. only allows to change chat's name.
    when more metadata to be added, this function will do more useful stuff"""

    try:
        chatID = request.config.get('id')
        if chatID is None:
            return Response({'Błąd': 'Nie podano ID chatu'}, status=status.HTTP_400_BAD_REQUEST)

        chat = chatDB.objects.filter(id=chatID).first()

        members = request.content.get('members')
        messages = request.content.get('messages')
        is_group_chat = request.content.get('is_group_chat')

        if (members is None or messages is None or is_group_chat is None or
            len(chat.members) != len(members) or
            len(chat.messages) != len(messages) or
            chat.is_group_chat != is_group_chat):

            return Response({'Błąd': 'Modyfikowanie wrażliwych danych'}, status=status.HTTP_403_FORBIDDEN)
        else:
            serializer = chatDBSerializer(chat, data=request.content, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                raise KeyError()

    except KeyError:
        return Response({'Błąd': 'Nie ma wszystkich parametrów (lub jest za dużo)'}, status=status.HTTP_400_BAD_REQUEST)

    except TypeError:
        return Response({'Błąd': 'Body nie jest w formacie JSON'}, status=status.HTTP_400_BAD_REQUEST)

    except ValueError:
        return Response({'Błąd': 'Nie ma chatu o takim ID lub format jednego z pól jest nieprawidłowy'}, status=status.HTTP_404_NOT_FOUND)

    except DatabaseError:
        return Response({'Błąd': 'Baza danych nie działa :('}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    except chatDB.DoesNotExist:
        return Response({'Błąd': 'Nie ma chatu o takim ID'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['PATCH'])
@check_api_key
def deleteUserFromChat(request):
    """Kicks user from chat"""

    try:
        if request.content.get('login') is None or request.content.get('id') is None:
            return Response({'Błąd': 'Nie podano loginu użytkownika lub ID chatu'}, status=status.HTTP_400_BAD_REQUEST)

        user = userDB.objects.filter(login=request.content.get('login')).first()
        chat = chatDB.objects.filter(id=request.content.get('id')).first()

        updated_user_list = user.included_in_these_chats
        updated_user_list.remove(request.content.get('id'))
        user.included_in_these_chats = updated_user_list
        user.save()

        updated_chat_members = chat.members

        for i in range(len(updated_chat_members)): # ilość członków w jednym chacie nie będzie większa niż maksymalnie 3 lub 4 tysiące, więc wyszukiwanie liniowe jest ok
            if updated_chat_members[i].get('login') == request.content.get('login'):
                updated_chat_members.pop(i)
                break

        chat.members = updated_chat_members
        chat.save()

        serializer = chatDBMembersSerializer(chat.members)

    except TypeError:
        return Response({'Błąd': 'Body nie jest w formacie JSON'}, status=status.HTTP_400_BAD_REQUEST)

    except ValueError:
        return Response({'Błąd': 'Nie ma chatu o takim ID lub format jednego z pól jest nieprawidłowy'}, status=status.HTTP_404_NOT_FOUND)

    except DatabaseError:
        return Response({'Błąd': 'Baza danych nie działa :('}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    except userDB.DoesNotExist:
        return Response({'Błąd': 'Nie ma użytkownika z takim loginem'}, status=status.HTTP_404_NOT_FOUND)

    except chatDB.DoesNotExist:
        return Response({'Błąd': 'Nie ma chatu o takim ID'}, status=status.HTTP_404_NOT_FOUND)

    else:
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)


# messages operations

@api_view(['POST'])
@check_api_key
def postMessage(request):
    """Posts messages from user to chat, that were provided"""