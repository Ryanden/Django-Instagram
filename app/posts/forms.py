
from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from posts.models import Post

User = get_user_model()


class PostForm(forms.Form):

    image = forms.ImageField()
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

        Post.objects.create(
            author=user,
            photo=photo,
            content=content,
        )
