from rest_framework import serializers
from location_app.models import LocationDB


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocationDB
        fields = "__all__"
