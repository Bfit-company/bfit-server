from django.db.models import Q, F, Value as V
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from location_app.models import LocationDB
from location_app.api.serializer import LocationSerializer
# from location_app.api.permissions import
from rest_framework.views import APIView


class LocationList(APIView):
    def get(self, request):
        location_list = LocationDB.objects.all()
        serializer = LocationSerializer(location_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = LocationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LocationDetail(APIView):
    # permission_classes = [PostUserOrReadOnly, AdminOrReadOnly]

    def get(self, request, pk):
        location = get_object_or_404(LocationDB, pk=pk)
        serializer = LocationSerializer(location)
        return Response(serializer.data)

    def put(self, request, pk):
        location = get_object_or_404(LocationDB, pk=pk)
        self.check_object_permissions(request, location)
        serializer = LocationSerializer(location, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        location = get_object_or_404(LocationDB, pk=pk)
        location.delete()
        return Response("Delete Successfully", status=status.HTTP_200_OK)
