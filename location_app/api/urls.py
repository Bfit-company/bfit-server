from django.urls import path, re_path
from location_app.api.views import (
    LocationList,
    LocationDetail,
    CountryList,
    CityList,
    CountryDetail,
    CityDetail,
    GetCoachesByCityName,
    GetCoachesWithLongLat
)

urlpatterns = [
    path('location_list/', LocationList.as_view(), name='location_list'),
    path('country_list/', CountryList.as_view(), name='country_list'),
    path('city_list/', CityList.as_view(), name='city_list'),
    path('location_detail/<int:pk>/', LocationDetail.as_view(), name='location_detail'),
    path('country_detail/<int:pk>/', CountryDetail.as_view(), name='country_detail'),
    path('city_detail/<int:pk>/', CityDetail.as_view(), name='city_detail'),
    path('get_coach_by_city_name/<str:city_name>/', GetCoachesByCityName.as_view(), name='get_coach_by_city_name'),
    path('get_coaches_with_long_lat/', GetCoachesWithLongLat.as_view(), name='get_coaches_with_long_lat'),
]
