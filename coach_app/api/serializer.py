from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField

from coach_app.models import CoachDB
from sport_type_app.api.serializer import SportTypeSerializer
from person_app.api.serializer import PersonSerializer
from datetime import date


class CoachSerializer(serializers.ModelSerializer):
    person = PersonSerializer(read_only=True)
    location_coach = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = CoachDB
        fields = "__all__"


    # def validate(self, value):
    #     if not self.validated_data.is_coach:
    #         raise serializers.ValidationError("the user have to be coach")
