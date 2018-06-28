from django import forms

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()


class SignupModelForm(forms.ModelForm):
    pass


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
        required=False,
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

    image_profile = forms.ImageField(
        required=False,
    )

    introduction = forms.CharField(
        required=False,
        label='자기소개',
        widget=forms.Textarea(
            attrs={
                'class': 'form-control'
            }
        )
    )

    gender = forms.ChoiceField(
        choices=(
            ('m', '남성'),
            ('f', '여성'),
            ('x', '선택안함'),
        )
    )

    site = forms.CharField(
        required=False,
        label='사이트',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        )
    )

    def clean_username(self):

        username = self.cleaned_data['username']
        reputation = User.objects.filter(username=username).exists()

        if reputation:
            raise ValidationError('이미 사용중인 아이디입니다.')

        return username

    def clean(self):
        super().clean()
        password = self.cleaned_data['password']
        password2 = self.cleaned_data['password2']

        if password != password2:
            self.add_error('password2', '비밀번호와 비밀번호 확인의 값이 일치하지 않습니다.')

        return self.cleaned_data

    def signup(self):
        fields = [
            'username',
            'email',
            'password',
            'img-profile',
            'introduction',
            'site',
        ]

        # create_user_dict = {key: value for key, value in self.cleaned_data.items() if key in fields}

        # def check(item):
        #     return item[0] in fields

        # create_user_dict = {}

        # create_user_dict = dict(filter(check, self.cleaned_data.items()))

        create_user_dict = dict(filter(lambda item: item[0] in fields, self.cleaned_data.items()))

        print(create_user_dict)

        user = User.objects.create_user(**create_user_dict)

        return user



