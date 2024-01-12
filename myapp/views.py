from rest_framework.decorators import api_view
from rest_framework.utils import json
from django.http import JsonResponse
from rest_framework import status
import json
from pydantic import ValidationError
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import UserSerializer, UserCreationSerializer
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .models import EmailConfirmationToken
from .functions import send_confirmation_email
from django.http import request


@api_view(['POST'])
def api_create_user(request):
    serializer = UserCreationSerializer(data=request.data)

    if serializer.is_valid():
        user = serializer.save()

        # email = serializer.validated_data.get('email', None)
        # token = EmailConfirmationToken.objects.create(user=user)
        # send_confirmation_email(email=user.email, token_id=token.pk, user_id=user.pk)
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SendUserConfirmationTokenAPIView(APIView):
    # permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        user = request.user
        token = EmailConfirmationToken.objects.create(user=user)
        send_confirmation_email(email=user.email, token_id=token.pk, user_id=user.pk)
        return Response(status=status.HTTP_200_OK)


def confirm_email_view(request):
    token_id = request.GET.get('token_id', None)
    user_id = request.GET.get('user_id', None)
    try:
        token = EmailConfirmationToken.objects.get(pk=token_id)
        user = token.user
        user.is_email_confirmed = True
        user.save()
        data = {'is_email_confirmed': False}
        return HttpResponse('success', status=status.HTTP_200_OK)
    except EmailConfirmationToken.DoesNotExist:
        data = {'is_email_confirmed': False}
        return render(request, template_name='confirm_email.html', context=data)

