from django.http import HttpResponse, JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
import requests
from rest_framework.utils import json
from django.core import serializers
from django.forms.models import model_to_dict

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
        return Response({'success': 'logout successfully'}, status=status.HTTP_200_OK)


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
            if UserDB.objects.filter(email=serializer.data['email']).exists():
                data['error'] = 'Email is already exist !'

            elif serializer.data['email'] == '' or \
                    serializer.data['password'] == '' or \
                    serializer.data['password2'] == '':
                data['error'] = 'Some field is blank !'
            return Response(data)

        return Response(data)


#
@api_view(['POST', ])
def liad(request):
    data = {}
    #
    # # create user
    # user_serializer = RegistrationSerializer(data=request.data['user'])
    # if user_serializer.is_valid():
    #     account = user_serializer.save()
    #
    # # if 'user' not in data:
    # #     qs = UserDB.objects.filter(email=request.data['user']['email'])
    # #     serializer = UserSerializer(qs)
    # #     account = serializer.data
    # data['user'] = {}
    # data['user']['email'] = account.email
    # data['user']['user_id'] = account.id
    # token = Token.objects.get(user=account).key
    # data['user']['token'] = token

    # create person
    person_obj = request.data['person']
    person_obj.update({'user': request.data['person']['user']})
    response = requests.post('http://127.0.0.1:8000/person/person_list/', data=person_obj)
    if response.status_code == status.HTTP_200_OK:
        person = json.loads(response.content)
    else:
        return JsonResponse(json.loads(response.content))


    # person_serializer = PersonSerializer(data=person_obj)
    # if person_serializer.is_valid():
    #     person_obj = person_serializer.save()
    # else:
    #     return Response(person_serializer.errors)

    # data["person"] = person_obj
    # # convert person to json
    # data["person"] = model_to_dict(data["person"])
    # data["person"] = json.loads(json.dumps(data["person"], indent=4, default=str))
    # check if the person is coach
    # if data['person'].is_coach:
    if request.data['coach']:
        # create coach
        data["coach"] = {}
        coach_obj = request.data['coach']
        coach_obj.update({'person': person["id"]})
        response = requests.post('http://127.0.0.1:8000/coach/coach_list/', data=coach_obj)
        if response.status_code == status.HTTP_200_OK:
            data['coach'] = json.loads(response.content)
        else:
            data['error'] = json.loads(response.content)

    if request.data['trainee']:
        # create coach
        data["trainee"] = {}
        trainee_obj = request.data['trainee']
        trainee_obj.update({'person': person["id"]})
        response = requests.post('http://127.0.0.1:8000/coach/coach_list/', data=trainee_obj)
        if response.status_code == status.HTTP_200_OK:
            data['trainee'] = json.loads(response.content)
        else:
            data['error'] = json.loads(response.content)

    return JsonResponse(data, safe=False)
    # return HttpResponse(data, content_type="application/json")
# todo:in futute
# @api_view(['POST', ])
# def login_view(request):
#     if request.method == 'POST':
#         # serializer = LoginSerializer(data=request.data)
#         token = Token.objects.get(user=account).key
#         print("######################################")
#         # print(request.user.data)
#         #update_last_login(None, request.user)
