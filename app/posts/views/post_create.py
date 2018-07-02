
from django.shortcuts import render, redirect

from posts.forms import PostModelForm


def post_create(request):

    if request.method == 'POST':
        form = PostModelForm(request.POST, request.FILES)

        post = form.save(commit=False)

        post.author = request.user

        post.save()

        return redirect('posts:post-list')

    form = PostModelForm()

    context = {
        'form': form
    }

    return render(request, 'posts/post_create.html', context)