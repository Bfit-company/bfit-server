from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from . import views
from user_app.api.views import registration_view
from user_app.api.views import logout_view,liad
# from user_app.api.views import login_view

urlpatterns = [
    path('login/', obtain_auth_token, name='login'),
    path('register/', registration_view, name='register'),
    path('liad/', liad, name='liad'),
    path('logout/', logout_view, name='logout')
]