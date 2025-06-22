from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db import DatabaseError
from rest_framework import status
from datetime import datetime # message date and time

from db.models import chatDB, userDB
from .serializers import chatDBSerializer, chatDBMessagesSerializer
from userAPI.serializers import userDBSerializer

from userAPI.views import check_api_key, contain_necessary_fields


@api_view(['POST'])
@check_api_key
def postMessage(request):
    """Posts messages from user to chat, that were provided"""