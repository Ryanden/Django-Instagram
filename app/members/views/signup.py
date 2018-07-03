from django.contrib.auth import login, get_user_model
from django.shortcuts import redirect, render

from members.forms import SignupForm


User = get_user_model()

__all__ = (
    'signup',
)


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
