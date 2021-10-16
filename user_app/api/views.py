from django.http import HttpResponse, JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
import requests
from rest_framework.utils import json
from django.core import serializers
from django.forms.models import model_to_dict

from person_app.api.serializer import PersonSerializer
from person_app.models import PersonDB
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
            data['id'] = account.id
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
def full_user_create(request):
    data = {}

    # create person
    person_obj = request.data['person']
    person_obj.update({'user': request.data['person']['user']})
    headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
    response = requests.post('http://127.0.0.1:8000/person/person_list/', data=json.dumps(person_obj), headers=headers)
    if response.status_code == status.HTTP_200_OK:
        person = json.loads(response.content)
    else:
        return JsonResponse(json.loads(response.content))

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
        response = requests.post('http://127.0.0.1:8000/trainee/trainee_list/', data=trainee_obj)
        if response.status_code == status.HTTP_200_OK:
            data['trainee'] = json.loads(response.content)
        else:
            data['error'] = json.loads(response.content)
    #
    if "error" in data.keys():
        PersonDB.objects.filter(id=person["id"]).delete()

    return JsonResponse(data, safe=False)
    # return HttpResponse(data, content_type="application/json")
