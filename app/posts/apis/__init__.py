# /api/posts/
# 1. posts.serializer -> PostSerializer
# 2. apis.__init__
#       class PostList(APIView):
#             def get(self, request):
#                 <logic>
# 3. config.urls 에서 (posts.urls 는 무시)
#   /api/posts/ 가 우의 PostList.as_view()와 연결되도록 처리


# /posts/       <- posts.views.post_list
# /api/posts/   <- posts.apis.PostList.as_view()

# 1. posts.serializer 에 PostSerializer 구현
# 2. apis 에 PostList GenericCBV 구현
# 3. posts.ulrs 를 분할
#         -> posts.urls.views
#         -> posts.urls.apis
# 4. config.urls 에서 적절히 include 처리
# 5. /api/posts/ 로 Postㅡ무 collenction 작성
# 6. 실행확인


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


class PostDetail(generics.ListAPIView):
    pass