from rest_framework.response import Response
from rest_framework.views import APIView
from ..models import Post
from ..serializer import PostBaseSerializer


class PostList(APIView):

    def get(self, request, format=None):
        post = Post.objects.all()
        serializer = PostBaseSerializer(post, many=True)

        return Response(serializer.data)
