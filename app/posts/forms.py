
from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from posts.models import Post

User = get_user_model()


class PostModelForm(forms.ModelForm):
    # 필드를 직접정의 하지 않음.
    class Meta:
        model = Post
        fields = ['photo', 'content']


class PostForm(forms.Form):

    image = forms.ImageField(
        widget=forms.FileInput(
            attrs={
                'class': 'form-control'
            }
        )
    )
    content = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'no-resize',
                'maxlength': 50,
                'placeholder': '내용을 입력해주세요.'
            }
        )
    )

    def upload_file(self, user):

        content = self.cleaned_data['content']
        photo = self.cleaned_data['image']

        post = Post.objects.create(
            author=user,
            photo=photo,
            content=content,
        )

        return post
