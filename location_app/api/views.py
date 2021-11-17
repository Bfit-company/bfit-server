from django.db.models import Q, F, Value as V
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from coach_app.models import CoachDB
from location_app.models import LocationDB, CountryDB, CityDB
from location_app.api.serializer import LocationSerializer, CitySerializer, CountrySerializer
# from location_app.api.permissions import
from rest_framework.views import APIView


class LocationList(APIView):
    def get(self, request):
        location_list = LocationDB.objects.all()
        serializer = LocationSerializer(location_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = LocationSerializer(data=request.data)
        city = request.data['city']
        country = city['country']
        if city:
            city_serializer = CitySerializer(data=city)
            if city_serializer.is_valid():
                city_serializer.save()
                print("city saved")
            else:
                return Response(city_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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


class CityList(APIView):
    def get(self, request):
        city_list = CityDB.objects.all()
        serializer = CitySerializer(city_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CitySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CityDetail(APIView):
    # permission_classes = [PostUserOrReadOnly, AdminOrReadOnly]

    def get(self, request, pk):
        city = get_object_or_404(CityDB, pk=pk)
        serializer = CitySerializer(city)
        return Response(serializer.data)

    def put(self, request, pk):
        city = get_object_or_404(CityDB, pk=pk)
        self.check_object_permissions(request, city)
        serializer = CitySerializer(city, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        city = get_object_or_404(CityDB, pk=pk)
        city.delete()
        return Response("Delete Successfully", status=status.HTTP_200_OK)


class CountryList(APIView):
    def get(self, request):
        country_list = CountryDB.objects.all()
        serializer = CountrySerializer(country_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CountrySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CountryDetail(APIView):
    # permission_classes = [PostUserOrReadOnly, AdminOrReadOnly]

    def get(self, request, pk):
        country = get_object_or_404(CountryDB, pk=pk)
        serializer = CountrySerializer(country)
        return Response(serializer.data)

    def put(self, request, pk):
        country = get_object_or_404(CountryDB, pk=pk)
        self.check_object_permissions(request, country)
        serializer = CountrySerializer(country, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        country = get_object_or_404(CountryDB, pk=pk)
        country.delete()
        return Response("Delete Successfully", status=status.HTTP_200_OK)

# def cityAndCountryCheck(country,city,long,lat):
#     if country and not CountryDB.objects.filter(english_name__iexact=country.lower()).exists():
#
