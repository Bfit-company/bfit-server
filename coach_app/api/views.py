from django.db.models import Q,F, Value as V
from django.db.models.functions import Concat
from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from coach_app.api.serializer import CoachSerializer
from coach_app.models import CoachDB
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from random import shuffle

from person_app.api.serializer import PersonSerializer
from person_app.models import PersonDB
from sport_type_app.models import SportTypeDB
from user_app import models


@api_view(['GET', 'POST'])
def coach_list(request):
    if request.method == 'GET':
        all_trainee_list = CoachDB.objects.all()
        serializer = CoachSerializer(all_trainee_list, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = CoachSerializer(data=request.data)
        if serializer.is_valid():
            person_id = request.data.get("person")
            person_check = CoachDB.objects.filter(person=person_id)
            person_coach = PersonDB.objects.get(pk=person_id)
            # check if the person is not coach
            if not person_coach.is_coach:
                return Response({"error": "the user is not coach"})
            if not person_check.exists():
                serializer.save(person=PersonDB.objects.get(pk=person_id))
                return Response(serializer.data)
            else:
                return Response({"error": "the coach already exist"})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'DELETE', 'PUT'])
def coach_detail(request, pk):
    if request.method == 'GET':
        trainee = get_object_or_404(CoachDB, pk=pk)
        serializer = CoachSerializer(trainee)
        return Response(serializer.data)

    if request.method == 'PUT':
        coach = get_object_or_404(CoachDB, pk=pk)
        serializer = CoachSerializer(coach, data=request.data)
        if serializer.is_valid():
            coach.person = get_object_or_404(PersonDB, pk=request.data["person"])
            coach.description = request.data["description"]
            coach.rating = request.data["rating"]
            coach.save()

            coach.fav_sport.set(request.data["fav_sport"])

            serializer = CoachSerializer(coach)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    if request.method == 'DELETE':
        trainee = get_object_or_404(CoachDB, pk=pk)
        trainee.delete()
        return Response("Delete Successfully", status=status.HTTP_200_OK)


# find trainee by full name (first 10 matches)
@api_view(['GET', 'DELETE', 'PUT'])
def find_coach_by_name(request, name):
    if request.method == 'GET':
        if name is None:
            return Response("name is empty")

        name = name.strip()
        trainees = CoachDB.objects.select_related('person').annotate(
            full_name=Concat('person__first_name', V(' '), 'person__last_name')).filter(
            Q(full_name__icontains=name) |
            Q(person__first_name=name) |
            Q(person__last_name=name))[:10]

        serializer = CoachSerializer(trainees, many=True)
        return Response(serializer.data)


# get coach list by sport type
@api_view(['GET'])
def coach_list_by_sport_type(request, pk):
    if request.method == 'GET':
        if pk is None:
            return Response("pk is empty")

        # get coach list by sport type
        coaches = list(CoachDB.objects.select_related('person').filter(
            Q(person__fav_sport=pk))[:10])
        shuffle(coaches)  # shuffle the query

        serializer = CoachSerializer(coaches, many=True)
        return Response(serializer.data)


# get coach list by rating
@api_view(['GET'])
def coach_list_sorted_by_rating(request):
    if request.method == 'GET':
        # get coach list by sport type
        coaches = list(CoachDB.objects.order_by("-rating")[:10])
        shuffle(coaches)  # shuffle the query
        serializer = CoachSerializer(coaches, many=True)
        return Response(serializer.data)


# get coach list by rating
@api_view(['GET'])
def coach_list_sorted_by_date_joined(request):
    if request.method == 'GET':
        # get coach list by sport type
        coaches = list(CoachDB.objects.order_by("-date_joined")[:10])
        shuffle(coaches)  # shuffle the query

        serializer = CoachSerializer(coaches, many=True)
        return Response(serializer.data)


MAX_LIMIT = 100


# get coach list search by parameters sort
@api_view(['GET'])
def coach_list_search_by_parameters(request):
    if request.method == 'GET':

        name = request.query_params.get("name")
        rating = request.query_params.get("rating")
        date_joined = request.query_params.get("date_joined")
        limit = request.query_params.get("limit")
        fav_sport = request.query_params.get("fav_sport")

        if date_joined == '':
            date_joined = '1900-01-01'
        if rating == '':
            rating = '1'
        if limit == '':
            limit = MAX_LIMIT  # max limit
        if fav_sport is '':  # if empty get all sport_type
            fav_sport = ~Q(person__fav_sport=None)  # not equal to None
        else:
            fav_sport = Q(person__fav_sport=fav_sport)

        name = name.strip()
        coaches = CoachDB.objects.select_related('person').annotate(
            full_name=Concat('person__first_name', V(' '), 'person__last_name')).filter(
            Q(full_name__icontains=name) |
            Q(person__first_name=name) |
            Q(person__last_name=name),
            Q(date_joined__gte=date_joined),
            Q(rating__gte=rating),
            fav_sport).order_by("-date_joined")[:int(limit)]

    serializer = CoachSerializer(coaches, many=True)
    return Response(serializer.data)
