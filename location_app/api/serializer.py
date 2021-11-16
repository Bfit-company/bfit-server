from rest_framework import serializers
from location_app.models import LocationDB, CountryDB, CityDB


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocationDB
        fields = "__all__"


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = CountryDB
        fields = "__all__"


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = CityDB
        fields = "__all__"
