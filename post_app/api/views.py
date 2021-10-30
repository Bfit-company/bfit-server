from django.db.models import Q, F, Value as V
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from post_app.models import PostDB
from post_app.api.serializer import PostSerializer



@api_view(['GET', 'POST'])
def post_list(request):
    if request.method == 'GET':
        posts_list = PostDB.objects.all()
        serializer = PostSerializer(posts_list, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


@api_view(['GET', 'DELETE', 'PUT'])
def post_detail(request, pk):
    if request.method == 'GET':
        post = get_object_or_404(PostDB, pk=pk)
        serializer = PostSerializer(post)
        return Response(serializer.data)

    if request.method == 'PUT':
        post = get_object_or_404(PostDB, pk=pk)
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    if request.method == 'DELETE':
        post = get_object_or_404(PostDB, pk=pk)
        post.delete()
        return Response("Delete Successfully", status=status.HTTP_200_OK)

