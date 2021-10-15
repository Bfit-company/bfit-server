from django.db.models.functions import Concat
from django.db.models import Value as V, Q
from django.http import HttpResponse
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes
from trainee_app.api.serializer import TraineeSerializer
from trainee_app.models import TraineeDB
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.core import serializers
from person_app.models import PersonDB
from person_app.api.serializer import PersonSerializer
from sport_type_app.models import SportTypeDB
from user_app import models



@api_view(['GET', 'POST'])
def trainee_list(request):
    if request.method == 'GET':
        all_trainee_list = TraineeDB.objects.all()
        serializer = TraineeSerializer(all_trainee_list, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = TraineeSerializer(data=request.data)
        if serializer.is_valid():
            person_check = TraineeDB.objects.filter(person=request.data.get("person"))
            if not person_check.exists():
                trainee_object = TraineeDB.objects.create(person=PersonDB.objects.get(pk=request.data["person"]))
                trainee_object.save()

                for fav in request.data["fav_sport"]:
                    fav_obj = SportTypeDB.objects.get(pk=fav)
                    trainee_object.fav_sport.add(fav_obj)

                serializer = TraineeSerializer(trainee_object)

            # serializer.save(person=PersonDB.objects.get(pk=request.data.get("person")),
            #                 fav_sport=SportTypeDB.objects.filter(id__in=request.data.get("fav_sport")))
            # serializer.save()
                return Response(serializer.data)
            else:
                return Response({"error": "the trainee already exist"})
        else:
            return Response(serializer.errors)



# class traineeVS(viewsets.ModelViewSet):
#     queryset = TraineeDB.objects.all()
#     serializer_class = TraineeSerializer


@api_view(['GET', 'DELETE', 'PUT'])
def trainee_detail(request, pk):
    if request.method == 'GET':
        trainee = get_object_or_404(TraineeDB, pk=pk)
        serializer = TraineeSerializer(trainee)
        return Response(serializer.data)

    if request.method == 'PUT':
        trainee = get_object_or_404(TraineeDB, pk=pk)
        serializer = TraineeSerializer(trainee, data=request.data)
        if serializer.is_valid():
            trainee.person = get_object_or_404(PersonDB, pk=request.data["person"])
            trainee.save()
            trainee.fav_sport.set(request.data["fav_sport"])

            serializer = TraineeSerializer(trainee)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    if request.method == 'DELETE':
        trainee = get_object_or_404(TraineeDB, pk=pk)
        trainee.delete()
        return Response("Delete Successfully", status=status.HTTP_200_OK)


# find trainee by full name (first 10 matches)
@api_view(['GET', 'DELETE', 'PUT'])
def find_trainee_by_name(request, name):
    if request.method == 'GET':
        if name is None:
            return Response("name is empty")
        name = name.strip()
        trainees = TraineeDB.objects.select_related('person').annotate(
            full_name=Concat('person__first_name', V(' '), 'person__last_name')).filter(
            Q(full_name__icontains=name) |
            Q(person__first_name=name) |
            Q(person__last_name=name))[:10]

        serializer = TraineeSerializer(trainees, many=True)
        return Response(serializer.data)
