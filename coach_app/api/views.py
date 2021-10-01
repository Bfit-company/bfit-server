from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from coach_app.api.serializer import CoachSerializer
from coach_app.models import CoachDB
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

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
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


@api_view(['GET', 'DELETE', 'PUT'])
def coach_detail(request, pk):
    if request.method == 'GET':
        trainee = get_object_or_404(CoachDB, pk=pk)
        serializer = CoachSerializer(trainee)
        return Response(serializer.data)

    if request.method == 'PUT':
        trainee = get_object_or_404(CoachDB, pk=pk)
        serializer = CoachSerializer(trainee, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    if request.method == 'DELETE':
        trainee = get_object_or_404(CoachDB, pk=pk)
        trainee.delete()
        return Response("Delete Successfully", status=status.HTTP_200_OK)
