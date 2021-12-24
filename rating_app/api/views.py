from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView

from coach_app.api.views import ChangeCoachRating
from coach_app.models import CoachDB
from person_app.models import PersonDB
from rating_app.api.serializer import GeneralRatingSerializer
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from user_app import models
from rating_app.models import RatingDB


def rating_handler(request, rating_obj=None, preview_rating=None):
    serializer = GeneralRatingSerializer(rating_obj, data=request.data)

    if serializer.is_valid():
        change_coach_rating_serializer, response = ChangeCoachRating().change_coach_rating(
            coach_id=request.data["rating_coach_id"],
            user_rating=request.data["rating"],
            request_method=request.method,
            preview_rating=preview_rating
        )

        if response.status_code == status.HTTP_200_OK:  # save, change or delete
            try:
                if request.method == "DELETE":
                    rating_obj.delete()
                    return Response("Delete Successfully", status=status.HTTP_200_OK)

                else:
                    serializer.save(person_id=PersonDB.objects.get(pk=request.data["person_id"]),
                                    rating_coach_id=CoachDB.objects.get(pk=request.data["rating_coach_id"]))
                    change_coach_rating_serializer.save()
                    return Response(change_coach_rating_serializer.data, status=status.HTTP_201_CREATED)
            except:
                return Response({"error": "user can not rating the same coach more than once"},
                                status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response(change_coach_rating_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RatingList(APIView):

    def get(self, request):
        # permission_classes = (IsAuthenticatedOrReadOnly,)
        rating_list = RatingDB.objects.all()
        serializer = GeneralRatingSerializer(rating_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        return rating_handler(request)
        # serializer = GeneralRatingSerializer(data=request.data)
        # if serializer.is_valid():
        #     change_coach_rating_serializer, response = ChangeCoachRating().change_coach_rating(
        #         coach_id=request.data["rating_coach_id"],
        #         user_rating=request.data["rating"],
        #         request_method=request.method)  # 'POST'
        #     if response.status_code == status.HTTP_200_OK:
        #         try:
        #             serializer.save(person_id=PersonDB.objects.get(pk=request.data["person_id"]),
        #                             rating_coach_id=CoachDB.objects.get(pk=request.data["rating_coach_id"]))
        #             change_coach_rating_serializer.save()
        #             return Response(change_coach_rating_serializer.data, status=status.HTTP_201_CREATED)
        #         except:
        #             return Response({"error": "user can not rating the same coach more than once"},
        #                             status=status.HTTP_400_BAD_REQUEST)
        #
        #     else:
        #         return Response(change_coach_rating_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # else:
        #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RatingDetail(APIView):

    def put(self, request):
        rating_obj = get_object_or_404(RatingDB,
                                       person_id=request.data["person_id"],
                                       rating_coach_id=request.data["rating_coach_id"])

        return rating_handler(request, rating_obj, rating_obj.rating)

    def delete(self, request):
        rating_obj = get_object_or_404(RatingDB,
                                       person_id=request.data["person_id"],
                                       rating_coach_id=request.data["rating_coach_id"])
        return rating_handler(request, rating_obj, rating_obj.rating)
