from django.db.models import Q, F, Value as V
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from post_app.models import PostDB
from post_app.api.serializer import PostSerializer
from post_app.api.permissions import PostUserOrReadOnly, AdminOrReadOnly
from rest_framework.views import APIView


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


class PostDetail(APIView):
    permission_classes = [PostUserOrReadOnly, AdminOrReadOnly]

    def get(self, request, pk):
        post = get_object_or_404(PostDB, pk=pk)
        serializer = PostSerializer(post)
        return Response(serializer.data)

    def put(self, request, pk):
        post = get_object_or_404(PostDB, pk=pk)
        self.check_object_permissions(request, post)
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        post = get_object_or_404(PostDB, pk=pk)
        post.delete()
        return Response("Delete Successfully", status=status.HTTP_200_OK)
