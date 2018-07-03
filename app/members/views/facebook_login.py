import requests
from django.contrib.auth import get_user_model, login
from django.shortcuts import redirect
from config import settings

User = get_user_model()

__all__ = (
    'facebook_login',
)


def facebook_login(request):
    # 1. access_token 을 얻음.
    def get_access_token(code):
        # GET parameter 의 'code'에 값이 전달됨 (authentication code)
        # 전달받은 인증코드를 사용해서 액세스토큰을 받음
        url = 'https://graph.facebook.com/v3.0/oauth/access_token?'

        params = {
            'client_id': settings.FACEBOOK_APP_ID,
            'redirect_uri': 'http://localhost:8000/members/facebook-login/',
            'client_secret': settings.FACEBOOK_APP_SECRET_CODE,
            'code': code,
        }
        response = requests.get(url, params)
        # 파이썬에 내장된 json 모듈을 사용해서, JSON 형식의 텍스트를 파이썬 Object 로 변환
        response_dict = response.json()

        # access_token 을 저장
        token = response_dict.get('access_token')
        return token

    def get_dubug_token(token):

        # 받은 액세스 토큰을 debug
        # 앱단에서 요청받는 토큰값이 유효한지 검사 할경우 debug 를 사용함
        # 결과에서 해당 토큰의 user_id(사용자 고유값)를 가져올 수 있음
        url = 'https://graph.facebook.com/debug_token?'
        params = {
            'input_token': token,
            'access_token': '{}|{}'.format(settings.FACEBOOK_APP_ID, settings.FACEBOOK_APP_SECRET_CODE),
        }

    # 2. access token 으로 user 정보를 얻음
    def get_user_info(token, fields=None):
        # GraphAPI 를 통해서 facebook user 의 정보 받아오기

        if fields is None:
            default_fields = ','.join([
                'id',
                'name',
                'first_name',
                'last_name',
                'picture',
            ])

        # fields = ['id', 'name', 'first_name', 'last_name', 'picture']

        url = 'https://graph.facebook.com/v3.0/me'

        params = {
            'fields': default_fields,
            'access_token': token,
        }

        response = requests.get(url, params)

        response_dict = response.json()

        return response_dict

    # 3. 전달받은 정보르 새로운 유저를 만듦
    def create_facebook_user(response_dict):
        # 받아온 정보 중 회원가입에 필요한 요소들 꺼내기
        facebook_user_id = response_dict.get('id')
        first_name = response_dict['first_name']
        last_name = response_dict['last_name']
        url_img_profile = response_dict['picture']['data']['url']

        user, user_create = User.objects.get_or_create(
            username=facebook_user_id,
            defaults={
                'first_name': first_name,
                'last_name': last_name
            }
        )

        if user_create:
            user.first_name = first_name
            user.last_name = last_name
            user.save()

        return user

    code = request.GET.get('code')

    access_token = get_access_token(code)

    user_info = get_user_info(access_token)

    user = create_facebook_user(user_info)

    login(request, user)

    return redirect('index')