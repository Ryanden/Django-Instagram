import requests
import json
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.shortcuts import render, redirect

# User 클래스를 가져올때는 get_user_model()
# Foreign Key 에 User 모델을 지정할때에는 settings.AUTO_USR_MODEL
from config import settings
from members.forms import SignupForm

User = get_user_model()

# Create your views here.


def login_view(request):
    # 1. members.urls <- members 로 include 되도록 config url 에 추가
    # 2. path 구현
    # 3. path 와 view 연결
    # 4. form 작성
    # 5. post 요청을 보내 뷰에서 잘 왔는지 확인
    # URL 'members/login/

    print('출력내용:', request.GET.get('next'))

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            print('성공')

            # authenticate 로 db 와 확인 request 세션값을 주고
            # session_id 값을 django_sessions 테이블에 저장, 데이터는 user 와 연결됨
            # 이 함수 실행 후 돌려줄 HTTP Response 에는 Set-Cookie 헤더를 추가, 내용은 session id= session 값
            login(request, user)

            next = request.GET.get('next')

            if next:
                return redirect(next)

            return redirect('posts:post-list')

        else:
            print('실패')
            return redirect('members:login')

    return render(request, 'members/login.html')


def logout_view(request):

    logout(request)
    return redirect('index')


def signup(request):

    if request.method == 'POST':
        form = SignupForm(request.POST, request.FILES)
        # 에러메시지가 없음
        if form.is_valid():
            user = form.signup()
            login(request, user)
            return redirect('index')
    # get 요청일 때 빈 form 을 전달해서 렌더링
    else:
        form = SignupForm()
    context = {
        'form': form,
    }
    return render(request, 'members/signup.html', context)


def withdraw(request):

    request.user.delete()

    return redirect('index')


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


def signup_bak(request):

    context = {
        'errors': [],
    }

    if request.method == 'POST':

        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        context['username'] = username
        context['email'] = email

        required_fields = {
            'username': {
                'verbose_name': '아이디',
            },
            'email': {
                'verbose_name': '이메일',
            },
            'password': {
                'verbose_name': '비밀번호',
            },
            'password2': {
                'verbose_name': '비밀번호 확인',
            },
        }

        for field_name in required_fields.keys():
            if not locals()[field_name]:
                context['errors'].append('{}을 채워주세요.'.format(
                    required_fields[field_name]['verbose_name']
                ))

        # 아이디가 중복일때
        if User.objects.filter(username=username).exists():
            context['errors'].append('이미 존재하는 아이디입니다')

        # 비밀번호가 서로 다를때
        if password != password2:
            context['errors'].append('패스워드가 일치하지 않습니다.')

        if not context['errors']:
            user = User.objects.create_user(username=username, password=password, email=email)

            login(request, user)

            return redirect('index')

        return render(request, 'members/signup_bak.html', locals())

    # get 요청일 경우
    return render(request, 'members/signup_bak.html', locals())


def follow_toggle(request):
    """
    Get 요청은 처리하지 않음
    Post 요청일 때,

    :param request:
    :return:
    """