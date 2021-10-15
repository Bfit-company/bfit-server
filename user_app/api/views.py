from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
import requests
from person_app.api.serializer import PersonSerializer
from user_app.api.serializer import RegistrationSerializer, UserSerializer
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import update_last_login
from rest_framework.authtoken.views import obtain_auth_token
from user_app.models import UserDB
from user_app.api.serializer import RegistrationSerializer
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


#
@api_view(['POST', ])
def liad(request):
    data = {}

    # create user
    user_serializer = RegistrationSerializer(data=request.data['user'])
    if user_serializer.is_valid():
        account = user_serializer.save()

    # if 'user' not in data:
    #     qs = UserDB.objects.filter(email=request.data['user']['email'])
    #     serializer = UserSerializer(qs)
    #     account = serializer.data
    data['user'] = {}
    data['user']['email'] = account.email
    data['user']['user_id'] = account.id
    token = Token.objects.get(user=account).key
    data['user']['token'] = token

    # create person
    data['person'] = {}
    person_obj = request.data['person']
    person_obj.update({'user': data['user']['user_id']})

    person_serializer = PersonSerializer(data=person_obj)
    if person_serializer.is_valid():
        person_obj = person_serializer.save()


    data["person"] = person_obj
    # check if the person is coach
    if data['person'].is_coach:
        # create coach
        data["coach"] = {}
        coach_obj = request.data['coach']
        coach_obj.update({'person': data['person'].id})
        response = requests.post('http://127.0.0.1:8000/coach/coach_list/', data=coach_obj)
        content = response.content
    else:
        data["trainee"] = {}
        trainee_obj = request.data['trainee']
        trainee_obj.update({'person': data['person'].id})
        # data["trainee"]["person"] = request.data["trainee"]["fav_sport"]
        response = requests.post('http://127.0.0.1:8000/trainee/trainee_list/', data=trainee_obj)
        content = response.content
        data["trainee"] = trainee_obj

    return Response(data)
# todo:in futute
# @api_view(['POST', ])
# def login_view(request):
#     if request.method == 'POST':
#         # serializer = LoginSerializer(data=request.data)
#         token = Token.objects.get(user=account).key
#         print("######################################")
#         # print(request.user.data)
#         #update_last_login(None, request.user)
