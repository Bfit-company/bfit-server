from rest_framework import serializers
from person_app.models import PersonDB
from datetime import date


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonDB
        fields = "__all__"

    # def validate_gender(self,value):
    #     if (value != 's'):
    #         raise serializers.ValidationError("liad")
    #     return "s"
    def validate_birth_date(self, value):
        if self.calculate_age(born=value) <= 12:
            raise serializers.ValidationError("Age must be 12 and above")
        return value

    # calculate the age
    def calculate_age(self, born):
        today = date.today()
        return today.year - born.year - ((today.month, today.day) < (born.month, born.day))