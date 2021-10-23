from rest_framework import serializers
from person_app.models import PersonDB
from datetime import date
from sport_type_app.api.serializer import SportTypeSerializer


class PersonRelatedField(serializers.StringRelatedField):
    def to_representation(self, value):
        return PersonSerializer(value, many=False).data

    def to_internal_value(self, data):
        return data


class PersonSerializer(serializers.ModelSerializer):
    fav_sport = SportTypeSerializer(many=True, read_only=True)

    class Meta:
        model = PersonDB
        fields = "__all__"

    # def validate_gender(self,value):
    #     if (value != 's'):
    #         raise serializers.ValidationError("liad")
    #     return "s"
    def validate_birth_date(self, value):
        if self.calculate_age(born=value) <= 13:
            raise serializers.ValidationError("Age must be 13 and above")
        return value

    # calculate the age
    def calculate_age(self, born):
        today = date.today()
        return today.year - born.year - ((today.month, today.day) < (born.month, born.day))
