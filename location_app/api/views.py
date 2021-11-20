import location as location
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q, F, Value as V
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from coach_app.models import CoachDB
from location_app.models import LocationDB, CountryDB, CityDB
from location_app.api.serializer import LocationSerializer, CitySerializer, CountrySerializer
from coach_app.api.serializer import CoachSerializer
# from location_app.api.permissions import
from rest_framework.views import APIView


def checkCountry(country):
    country_obj = CountryDB.objects.filter(name=country['name'])
    if not country_obj.exists():
        country_obj = CountryDB(name=country['name'])
        country_obj.save()
    else:
        country_obj = country_obj.first()
    return country_obj


def checkCity(city):
    if city:
        city_serializer = CitySerializer(data=city)
        city_obj = CityDB.objects.filter(name=city['name'],
                                         country=city['country'])
        if not city_obj.exists():
            if city_serializer.is_valid():
                city_obj = city_serializer.save()
                print("city saved")
        else:
            city_obj = city_obj.first()
        return city_obj
    return None



class LocationList(APIView):
    def get(self, request):
        location_list = LocationDB.objects.all()
        serializer = LocationSerializer(location_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        city = request.data['city']
        country = city['country']

        country_obj = checkCountry(country)
        city['country'] = int(country_obj.pk)
        city_obj = checkCity(city)

        # else:
        #     return Response(city_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        location_obj = request.data
        city_pk = int(city_obj.pk)
        location_obj.update({"city": city_pk})
        #
        # if location_obj['lat'] is None and location_obj['long'] is None:
        #     if isCoachInCity(city=location_obj['city'], coach_id=location_obj['coach']):
        #         return Response("this location is already exists", status=status.HTTP_404_NOT_FOUND)
        # else:
        #     if isLongAndLatExist(long=location_obj['long'], lat=location_obj['lat']):
        #         return Response("this location is already exists", status=status.HTTP_404_NOT_FOUND)

        # location_obj.update({"country": city['country']})
        serializer = LocationSerializer(data=location_obj)
        if serializer.is_valid():
            try:
                serializer.save(coach=CoachDB.objects.get(pk=request.data['coach']), city=CityDB.objects.get(pk=city_pk))
            except ObjectDoesNotExist:
                return Response("not found", status=status.HTTP_404_NOT_FOUND)
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


class GetCoachesByCityName(APIView):
    def get(self, request, city_name):
        if city_name is None:
            return Response("city name is empty")

        query_coach_list = LocationDB.objects.select_related('city', 'coach').filter(
                Q(city__name=city_name)).values('coach').distinct()
        # c = CoachDB.objects.get(pk=coaches)
        my_filter_qs = Q()
        for query in query_coach_list:
            my_filter_qs = my_filter_qs | Q(id=query['coach'])
        coaches = CoachDB.objects.filter(my_filter_qs)
        serializer = CoachSerializer(coaches, many=True)
        return Response(serializer.data)
