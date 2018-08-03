from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.compat import authenticate
from rest_framework.exceptions import AuthenticationFailed, NotAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..serializer import UserSerializer
from rest_framework import generics

User = get_user_model()


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class AuthToken(APIView):

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)

        if user:
            token, __ = Token.objects.get_or_create(user=user)
            data = {
                'token': token.key,
            }
            return Response(data)
        raise AuthenticationFailed('인증 정보가 올바르지 않습니다.')


class AuthenticationTest(APIView):

    def get(self, request):
        if request.user.is_authenticated:
            return Response(UserSerializer(request.user).data)

        raise NotAuthenticated('로그인 되어있지 않습니다.')
