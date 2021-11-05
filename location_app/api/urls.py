from django.urls import path, re_path
from location_app.api.views import (
    LocationList,
    LocationDetail
)

urlpatterns = [
    path('location_list/', LocationList.as_view(), name='location_list'),
    path('location_detail/<int:pk>/', LocationDetail.as_view(), name='location_detail'),
]
