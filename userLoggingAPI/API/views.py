from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db import DatabaseError
from rest_framework import status
from db.models import dbModel
from .serializers import dbModelSerializer

from functools import wraps
from userLoggingAPI.settings import BASE_DIR

import environ
import json

def check_api_key(view):
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
            return Response({'Błąd': 'Błędny klucz API'}, status=status.HTTP_401_UNAUTHORIZED)

        return view(request, *args, **kwargs)

    return wrapper

@api_view(['POST'])
@check_api_key
def register(request):
    """Add user to the database"""

    content = json.loads(request.data["_content"])

    try:
        for param in ('email', 'login', 'name', 'password', 'surname'):
            if content.get(param) is None:
                raise KeyError()

        login = content.get('login')
        email = content.get('email')

        for i in login:
            if i == " ":
                return Response({'Błąd': 'Login zawiera spacje'}, status=status.HTTP_400_BAD_REQUEST)

        if dbModel.objects.filter(login=login).first() is not None:
            return Response({'Błąd': 'Taki login już istnieje'}, status=status.HTTP_400_BAD_REQUEST)

        if dbModel.objects.filter(email=email).first() is not None:
            return Response({'Błąd': 'Podany email został już przypisany'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = dbModelSerializer(data=content)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            raise KeyError()

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

    content = json.loads(request.data["_content"])

    try:
        for param in ('login', 'password'):
            if content.get(param) is None:
                raise KeyError()

        user = dbModel.objects.get(login=content.get('login'))

        if user.password != content.get('password'):
            return Response({'Błąd': 'Złe hasło'}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = dbModelSerializer(user)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    except KeyError:
        return Response({'Błąd': 'Nie ma wszystkich parametrów (lub jest za dużo)'}, status=status.HTTP_400_BAD_REQUEST)
    
    except TypeError:
        return Response({'Błąd': 'Body nie jest w formacie JSON'}, status=status.HTTP_400_BAD_REQUEST)

    except ValueError:
        return Response({'Błąd': 'Format jednego z pól jest nieprawidłowy'}, status=status.HTTP_400_BAD_REQUEST)

    except DatabaseError:
        return Response({'Błąd': 'Baza danych nie działa :('}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    except dbModel.DoesNotExist:
        return Response({'Błąd': 'Taki login nie istnieje'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['DELETE'])
def delete_user(request):
    pass