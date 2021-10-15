from django.db.models import Q,Value as V
from django.db.models.functions import Concat
from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from coach_app.api.serializer import CoachSerializer
from coach_app.models import CoachDB
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

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
            person_check = CoachDB.objects.filter(person=request.data.get("person"))
            if not person_check.exists():
                coach_object = CoachDB.objects.create(
                    person=PersonDB.objects.get(pk=request.data["person"]),
                    rating=request.data["rating"],
                    description=request.data["description"]
                )

                for fav in request.data["fav_sport"]:
                    fav_obj = SportTypeDB.objects.get(pk=fav)
                    coach_object.fav_sport.add(fav_obj)
                coach_object.save()

                serializer = CoachSerializer(coach_object)

                # serializer.save(person=PersonDB.objects.get(pk=request.data.get("person")),
                #                 fav_sport=SportTypeDB.objects.filter(id__in=request.data.get("fav_sport")))
                # serializer.save()
                return Response(serializer.data)
            else:
                return Response({"error": "the coach already exist"})
        else:
            return Response(serializer.errors)


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