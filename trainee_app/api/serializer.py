from rest_framework import serializers
from trainee_app.models import TraineeDB
from sport_type_app.api.serializer import SportTypeSerializer
from person_app.api.serializer import PersonSerializer
from datetime import date


class TraineeSerializer(serializers.ModelSerializer):
    # sport_type = SportTypeSerializer(many=True, read_only=True)
    # person = PersonSerializer(many=False, read_only=True)

    class Meta:
        model = TraineeDB
        fields = "__all__"
