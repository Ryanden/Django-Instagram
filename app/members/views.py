from django.contrib.auth import authenticate, login, logout, get_user_model

from django.shortcuts import render, redirect

# User 클래스를 가져올때는 get_user_model()
# Foreign Key 에 User 모델을 지정할때에는 settings.AUTO_USR_MODEL
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

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            print('성공')

            login(request, user)

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
