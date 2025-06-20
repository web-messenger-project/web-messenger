from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db import DatabaseError
from rest_framework import status
from db.models import chatDB
from .serializers import chatDBSerializer
from userAPI.views import check_api_key

from functools import wraps
from API.settings import BASE_DIR

import json

@api_view(['GET'])
@check_api_key
def getMessages(request):
    pass