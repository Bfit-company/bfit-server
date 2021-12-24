from rest_framework import serializers
from coach_app.models import CoachDB
from rating_app.api.serializer import RatesSerializer
from person_app.api.serializer import PersonSerializer


class CoachSerializer(serializers.ModelSerializer):
    person = PersonSerializer(read_only=True)
    rates = serializers.SerializerMethodField()


    class Meta:
        model = CoachDB
        fields = "__all__"

    def get_rates(self, obj):
        return RatesSerializer(obj.rates.all(), many=True).data