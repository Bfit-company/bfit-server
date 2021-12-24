from django.urls import path

from sport_type_app.api.views import sport_type_detail_view
from .views import RatingList, RatingDetail

urlpatterns = [
    path('rating_list/', RatingList.as_view(), name='rating_list'),
    path('rating_detail/', RatingDetail.as_view(), name='rating_detail'),
]