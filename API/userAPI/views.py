from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db import DatabaseError
from rest_framework import status

from db.models import userDB
from .serializers import userDBSerializer

from functools import wraps
from API.settings import BASE_DIR

import environ
import json


def contain_necessary_fields(content: dict, params: tuple) -> bool: # function to iterate over request parameter and validate them
    for param in params:
        if content.get(param) is None:
            return False
    return True



def check_api_key(view): # decorator that checks for api key in request
    @wraps(view)
    def wrapper(request, *args, **kwargs):
        env = environ.Env()
        env.read_env(BASE_DIR / '.env')

        api_key = env('API_KEY')

        q = None
        if "_content" in request.data:
            try:
                content = json.loads(request.data["_content"])
                q = content.get("q")
            except Exception:
                q = None
        else:
            q = request.data.get("q")

        if q != api_key:
            return Response({'Błąd': 'Błędny klucz API lub niepoprawnie stworzony plik JSON, sprawdź czy na pewno na końcu ostatniego parametru nie ma przecinka'}, status=status.HTTP_401_UNAUTHORIZED)

        request.content = content

        return view(request, *args, **kwargs)

    return wrapper



@api_view(['POST'])
@check_api_key
def register(request):
    """Add user to the database"""

    try:
        if not contain_necessary_fields(request.content, ('email', 'login', 'name', 'password', 'surname')):
            raise KeyError()

        login = request.content.get('login')
        email = request.content.get('email')

        for i in login:
            if i == " ":
                return Response({'Błąd': 'Login zawiera spacje'}, status=status.HTTP_400_BAD_REQUEST)

        for param in ('name', 'surname', 'login'):
            if request.content.get(param) in ('SERVER', 'server', 'Server', 'SERWER', 'serwer', 'Serwer'):
                return Response({'Błąd': 'Użytkownik chce sie nazwać "SERVER"'}, status=status.HTTP_403_FORBIDDEN)

        if userDB.objects.filter(login=login).first() is not None:
            return Response({'Błąd': 'Taki login już istnieje'}, status=status.HTTP_400_BAD_REQUEST)

        if userDB.objects.filter(email=email).first() is not None:
            return Response({'Błąd': 'Podany email został już przypisany'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = userDBSerializer(data=request.content)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({'Błąd': 'Nie ma wszystkich pól, jest ich za dużo lub są w nieprawidłowym formacie'}, status=status.HTTP_400_BAD_REQUEST)

    except KeyError:
        return Response({'Błąd': 'Nie ma wszystkich parametrów (lub jest ich za dużo)'}, status=status.HTTP_400_BAD_REQUEST)

    except TypeError:
        return Response({'Błąd': 'Body nie jest w formacie JSON'}, status=status.HTTP_400_BAD_REQUEST)

    except ValueError:
        return Response({'Błąd': 'Format jednego z pól jest nieprawidłowy'}, status=status.HTTP_400_BAD_REQUEST)

    except DatabaseError:
        return Response({'Błąd': 'Baza danych nie działa :('}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['POST'])
@check_api_key
def login(request):
    """Retrive user data from the database"""

    try:
        if not contain_necessary_fields(request.content, ('login', 'password')):
            raise KeyError()

        user = userDB.objects.get(login=request.content.get('login'))

        if user.password != request.content.get('password'):
            return Response({'Błąd': 'Złe hasło'}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = userDBSerializer(user)

        return Response(serializer.data, status=status.HTTP_200_OK)

    except KeyError:
        return Response({'Błąd': 'Nie ma wszystkich parametrów (lub jest za dużo)'}, status=status.HTTP_400_BAD_REQUEST)

    except TypeError:
        return Response({'Błąd': 'Body nie jest w formacie JSON'}, status=status.HTTP_400_BAD_REQUEST)

    except ValueError:
        return Response({'Błąd': 'Format jednego z pól jest nieprawidłowy'}, status=status.HTTP_400_BAD_REQUEST)

    except DatabaseError:
        return Response({'Błąd': 'Baza danych nie działa :('}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    except userDB.DoesNotExist:
        return Response({'Błąd': 'Taki login nie istnieje'}, status=status.HTTP_404_NOT_FOUND)



@api_view(['POST'])
@check_api_key
def delete_user(request):
    """Permanently removes user account"""

    try:
        user_login = request.content.get('login')
        if user_login is None:
            return Response({'Błąd': 'Nie podano loginu użytkownika'}, status=status.HTTP_400_BAD_REQUEST)

        user = userDB.objects.filter(login=user_login).first()
        copy = user
        user.delete()

        serializer = userDBSerializer(copy)

    except KeyError:
        return Response({'Błąd': 'Nie ma wszystkich parametrów (lub jest za dużo)'}, status=status.HTTP_400_BAD_REQUEST)

    except TypeError:
        return Response({'Błąd': 'Body nie jest w formacie JSON'}, status=status.HTTP_400_BAD_REQUEST)

    except ValueError:
        return Response({'Błąd': 'Format jednego z pól jest nieprawidłowy'}, status=status.HTTP_400_BAD_REQUEST)

    except DatabaseError:
        return Response({'Błąd': 'Baza danych nie działa :('}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    except userDB.DoesNotExist:
        return Response({'Błąd': 'Taki login nie istnieje'}, status=status.HTTP_404_NOT_FOUND)

    else:
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)



@api_view(['POST'])
@check_api_key
def getAllUsers(request):
    """Returns data about each user"""

    try:
        users = userDB.objects.all()
        serializer = userDBSerializer(users, many=True)

    except TypeError:
        return Response({'Błąd': 'Nie ma użytkowników w bazie danych'}, status=status.HTTP_404_NOT_FOUND)
    
    except DatabaseError:
        return Response({'Błąd': 'Baza danych nie działa :('}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    else:
        return Response(serializer.data, status=status.HTTP_200_OK)