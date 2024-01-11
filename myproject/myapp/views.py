from rest_framework.decorators import api_view
from rest_framework.utils import json
from django.http import JsonResponse
from rest_framework import status
import json
from pydantic import ValidationError
from django.http import HttpResponse
from rest_framework.response import Response
from .serializers import UserSerializer, UserCreationSerializer
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


@api_view(['POST'])
def api_create_user(request):
    serializer = UserCreationSerializer(data=request.data)

    if serializer.is_valid():
        user = serializer.save()
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
