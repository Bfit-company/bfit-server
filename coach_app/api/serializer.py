from rest_framework import serializers
from coach_app.models import CoachDB
from sport_type_app.api.serializer import SportTypeSerializer
from person_app.api.serializer import PersonSerializer
from datetime import date


class CoachSerializer(serializers.ModelSerializer):
    fav_sport = SportTypeSerializer(many=True, read_only=True)
    person = PersonSerializer(many=False, read_only=True)

    class Meta:
        model = CoachDB
        fields = "__all__"


def validate_person(self, value):
    if not self.person.is_coach():
        raise serializers.ValidationError("the user have to be coach")