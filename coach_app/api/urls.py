from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from . import views
from user_app.api.views import registration_view
from user_app.api.views import logout_view
from coach_app.api.views import coach_list , coach_detail, find_coach_by_name

urlpatterns = [
    path('coach_list/', coach_list, name='coach_list'),
    path('coach_detail/<int:pk>/', coach_detail, name='coach_detail'),
    path('find_coach_by_name/<str:name>/', find_coach_by_name, name='find_coach_by_name'),
]