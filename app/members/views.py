from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.shortcuts import render, redirect

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

    if request.method == 'POST':

        print('로그아웃 성공')
        logout(request)

        return redirect('posts:post-list')

    else:
        print('로그아웃 실패')
        return redirect('posts:post-list')