from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from trainee_app.api.serializer import TraineeSerializer
from trainee_app.models import TraineeDB
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

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
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


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
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    if request.method == 'DELETE':
        trainee = get_object_or_404(TraineeDB, pk=pk)
        trainee.delete()
        return Response("Delete Successfully", status=status.HTTP_200_OK)

@api_view(['GET', 'DELETE', 'PUT'])
def find_trainee_by_name(request):
    if request.method == 'GET':
        trainees = TraineeDB.objects.select_related('person')
        for trainee in trainees:
            print(trainee.person.birth_date , trainee.person.first_name)
        # serializer = TraineeSerializer(trainee)
        return Response("trainee.data")