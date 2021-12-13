from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField

from coach_app.models import CoachDB
# from location_app.api.serializer import LocationSerializer
from sport_type_app.api.serializer import SportTypeSerializer
from person_app.api.serializer import PersonSerializer
from datetime import date


class CoachSerializer(serializers.ModelSerializer):
    person = PersonSerializer(read_only=True)
    # location_coach = LocationSerializer(many=True, read_only=True)

    class Meta:
        model = CoachDB
        fields = "__all__"

    # def update(self, instance, validated_data):
    #     nested_serializer = self.fields['person']
    #     nested_instance = instance.profile
    #     # note the data is `pop`ed
    #     nested_data = validated_data.pop('person')
    #     nested_serializer.update(nested_instance, nested_data)
    #     # this will not throw an exception,
    #     # as `profile` is not part of `validated_data`
    #     return super(CoachSerializer, self).update(instance, validated_data)

    # def validate(self, value):
    #     if not self.validated_data.is_coach:
    #         raise serializers.ValidationError("the user have to be coach")
