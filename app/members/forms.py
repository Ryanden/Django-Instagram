from django import forms

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()


class SignupForm(forms.Form):

    username = forms.CharField(
        label='아이디',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        )
    )
    email = forms.EmailField(
        label='이메일',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        )
    )
    password = forms.CharField(
        label='비밀번호',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control'
            }
        )
    )
    password2 = forms.CharField(
        label='비밀번호확인',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control'
            }
        )
    )

    def clean_username(self):

        username = self.cleaned_data['username']

        reputation = User.objects.filter(username=username).exists()

        if reputation:
            print('아이디 중복')
            raise ValidationError('중복값 있음')

        return username

    def clean_password(self):

        password = self.cleaned_data['password']

        password2 = self.cleaned_data.get('password2')

        if password != password2:
            print('비밀번호가 일치하지 않음')
            raise ValidationError('비밀번호 불일치')

        return password




