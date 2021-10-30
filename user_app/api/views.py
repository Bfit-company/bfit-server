from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ObjectDoesNotExist
from django.core.serializers import serialize
from django.http import HttpResponse, JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
import requests
from rest_framework.utils import json
from django.core import serializers
from django.forms.models import model_to_dict
from django.db.models import Q, F, Value as V

from coach_app.api.serializer import CoachSerializer
from coach_app.models import CoachDB
from person_app.api.serializer import PersonSerializer
from person_app.models import PersonDB
from trainee_app.api.serializer import TraineeSerializer
from trainee_app.models import TraineeDB
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
from rest_framework.authtoken.views import obtain_auth_token

User = get_user_model()


@api_view(['POST', ])
def logout_view(request):
    if request.method == 'POST':
        request.user.auth_token.delete()
        return Response({'success': 'logout successfully'}, status=status.HTTP_200_OK)


@api_view(['POST', ])
def login(request):
    if request.method == 'POST':
        data = {}
        try:
            user = UserDB.objects.get(email=request.data["username"])  # get the user_id
        except ObjectDoesNotExist:
            data['error'] = "the user does exist"
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        user_id = user.id
        is_coach = False
        try:
            coach = CoachDB.objects.select_related('person').get(Q(person__user=user_id))
            if coach:  # check if the coach exists
                serializer = CoachSerializer(coach)
                data['coach'] = serializer.data
                is_coach = True
        except ObjectDoesNotExist:
            is_coach = False
            print("coach not exist")

        if not is_coach:
            try:
                trainee = TraineeDB.objects.select_related('person').get(Q(person__user=user_id))
                if trainee:  # check if the trainee exists
                    serializer = TraineeSerializer(trainee)
                    data['trainee'] = serializer.data
                    is_coach = False
            except ObjectDoesNotExist:
                data['error'] = "the user do not finish the registration"
                data['user_id'] = user_id
                return Response(data, status=status.HTTP_400_BAD_REQUEST)

        token, created = Token.objects.get_or_create(user=user)
        data["token"] = token.key
        return JsonResponse(data)


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
            else:
                data['error'] = 'invalid field'
            return Response(data)

        return Response(data)


#
@api_view(['POST', ])
def full_user_create(request):
    data = {}
    BASEURL = 'http://' + get_current_site(request).domain + '/'
    # create person
    person_obj = request.data['person']
    person_obj.update({'user': request.data['person']['user']})
    headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
    response = requests.post(BASEURL + 'person/person_list/', data=json.dumps(person_obj), headers=headers)
    if response.status_code == status.HTTP_200_OK:
        person = json.loads(response.content)
    else:
        return JsonResponse(json.loads(response.content))

    # check if is coach
    if request.data['person']['is_coach']:
        # create coach
        data["coach"] = {}
        coach_obj = {}
        # coach_obj = request.data['coach']
        coach_obj.update({'person': person["id"]})
        response = requests.post(BASEURL + 'coach/coach_list/', data=coach_obj)
        if response.status_code == status.HTTP_200_OK:
            data['coach'] = json.loads(response.content)
        else:
            data['error'] = json.loads(response.content)

    elif not request.data['person']['is_coach']:
        # create trainee
        data["trainee"] = {}
        # trainee_obj = request.data['trainee']
        trainee_obj = {}
        trainee_obj.update({'person': person["id"]})
        response = requests.post(BASEURL + 'trainee/trainee_list/', data=trainee_obj)
        if response.status_code == status.HTTP_200_OK:
            data['trainee'] = json.loads(response.content)
        else:
            data['error'] = json.loads(response.content)
    # if there is some error while create trainee or coach delete person
    if "error" in data.keys():
        PersonDB.objects.filter(id=person["id"]).delete()

    return JsonResponse(data, safe=False)
