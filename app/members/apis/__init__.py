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


class FacebookAuthToken(APIView):
    def post(self, request):
        print('data 출력: ', request.data)

        facebook_id = request.data.get('facebook_id')
        last_name = request.data.get('last_name')
        first_name = request.data.get('first_name')

        user, __ = User.objects.get_or_create(
            username=facebook_id,
            defaults={
                'last_name': last_name,
                'first_name': first_name,
            }
        )

        # if User.objects.filter(username=facebook_id).exists():
        #     user = User.objects.get(username=facebook_id)
        #
        # else:
        #     user =User.objects.create_user(
        #         username=facebook_id,
        #         first_name=first_name,
        #         last_name=last_name,
        #     )
        token, __ = Token.objects.get_or_create(user=user)
        data = {
            'token': token.key,
            'user': UserSerializer(user).data
        }
        return Response(data)

        # raise AuthenticationFailed('인증 정보가 올바르지 않습니다.')

        # raise AuthenticationFailed('인증 정보가 올바르지 않습니다.')

        # request.data 에 'facebook_id' 와 'first-name, last-name' 이 올 것으로 예상
        # 전달받은 facebook_id에 해당하는 유저가 존재 한다면 해당 User 의 토큰값을 반환
        # 존재하지 않든다면 first_name 과 last_name 값을 추가로 사용해 생성한 User 에
        #   -> 해당하는 Token 을 가져오거나 새로 생성해서 리턴


class Profile(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            return Response(UserSerializer(request.user).data)

        raise NotAuthenticated('인증 되어 있지 않습니다.')
        # request.user 가 인증되어 있으면
        # UserSerializer 로 serialize 한 결과를 리턴
        # 인증이 되어있지 않다면 HttpNotAuthorized 예외 발생

