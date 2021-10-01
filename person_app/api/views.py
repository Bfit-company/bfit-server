from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view,permission_classes
from person_app.api.serializer import PersonSerializer
from person_app.models import PersonDB
from rest_framework.response import Response


from user_app import models

@api_view(['GET', 'POST'])
def person_list(request):
    if request.method == 'GET':
        all_trainee_list = PersonDB.objects.all()
        serializer = PersonSerializer(all_trainee_list, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = PersonSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


@api_view(['GET', 'DELETE', 'PUT'])
def person_detail(request, pk):
    if request.method == 'GET':
        trainee = get_object_or_404(PersonDB, pk=pk)
        serializer = PersonSerializer(trainee)
        return Response(serializer.data)

    if request.method == 'PUT':
        trainee = get_object_or_404(PersonDB, pk=pk)
        serializer = PersonSerializer(trainee, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    if request.method == 'DELETE':
        trainee = get_object_or_404(PersonDB, pk=pk)
        trainee.delete()
        return Response("Delete Successfully", status=status.HTTP_200_OK)


# @api_view(['GET', 'DELETE', 'PUT'])
# def find_person_by_name(request, pk):
#     if request.method == 'GET':
#         try:
#             PersonDB.objects.get(first_name=pk)
#         trainee = (PersonDB, pk=pk)
#         serializer = PersonSerializer(trainee)
#         return Response(serializer.data)

