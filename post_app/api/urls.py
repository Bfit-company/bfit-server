from django.urls import path, re_path
from post_app.api.views import (
    post_list,
    post_detail
)

urlpatterns = [
    path('post_list/', post_list, name='post_list'),
    path('post_detail/<int:pk>/', post_detail, name='post_detail'),
]
