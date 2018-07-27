from rest_framework.response import Response
from rest_framework.views import APIView
from ..models import Post
from ..serializer import PostBaseSerializer
from rest_framework import generics


class PostList(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostBaseSerializer


class PostCreate(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostBaseSerializer
