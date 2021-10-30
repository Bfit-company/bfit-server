from rest_framework import serializers
from coach_app.models import CoachDB
from post_app.models import PostDB
from sport_type_app.api.serializer import SportTypeSerializer
from person_app.api.serializer import PersonSerializer
from datetime import date


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = PostDB
        fields = "__all__"

