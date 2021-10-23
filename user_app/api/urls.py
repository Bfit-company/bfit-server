from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from . import views
from user_app.api.views import registration_view
from user_app.api.views import logout_view,full_user_create,login
# from user_app.api.views import login_view

urlpatterns = [
    path('login/', login, name='login'),
    path('register/', registration_view, name='register'),
    path('full_user_create/', full_user_create, name='full_user_create'),
    path('logout/', logout_view, name='logout')
]