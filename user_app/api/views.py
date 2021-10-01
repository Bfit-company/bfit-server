from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view,permission_classes
from user_app.api.serializer import RegistrationSerializer
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import update_last_login
from rest_framework.authtoken.views import obtain_auth_token

from user_app import models


@api_view(['POST', ])
def logout_view(request):
    if request.method == 'POST':
            request.user.auth_token.delete()
            return Response({'error': 'logout successfully'}, status=status.HTTP_200_OK)


@api_view(['POST', ])
def registration_view(request):
    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)

        data = {}

        if serializer.is_valid():
            account = serializer.save()
            data['email'] = account.email
            token = Token.objects.get(user=account).key
            data['token'] = token
            data['response'] = 'Registration Successful'

        else:
            data = serializer.errors

        return Response(data)



#todo:in futute
# @api_view(['POST', ])
# def login_view(request):
#     if request.method == 'POST':
#         # serializer = LoginSerializer(data=request.data)
#         token = Token.objects.get(user=account).key
#         print("######################################")
#         # print(request.user.data)
#         #update_last_login(None, request.user)
#         return Response("l")