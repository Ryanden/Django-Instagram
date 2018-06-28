from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseNotAllowed
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.views.decorators.http import require_POST

from posts.forms import PostForm, PostModelForm
from .models import Post


def post_list(request):

    posts = Post.objects.all()

    context = {
        'post_list': posts
    }

    return render(request, 'posts/post_list.html', context)


def post_detail(request, pk):

    post = Post.objects.get(pk=pk)

    context = {
        'post_detail': post
    }

    return render(request, 'posts/post_detail.html', context)


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




@login_required()
def post_create_with_form(request):

    if request.method == 'POST':

        form = PostForm(request.POST, request.FILES)

        if form.is_valid():

            print('유효함')

            post = form.upload_file(request.user)

            return redirect('posts:post-detail', pk=post.pk)

    else:

        if not request.user.is_authenticated:
            return redirect('members:login')

        form = PostForm()
    context = {
        'form': form,
    }
    return render(request, 'posts/post_create.html', context)


@require_POST
@login_required
def post_delete(request, pk):

    # another method

    # if request.method != 'POST':
    #     return HttpResponseNotAllowed()
    # if not request.user.is_authenticated:
    #     return redirect('members:login')

    post = get_object_or_404(Post, pk=pk)

    user = post.author

    if user != request.user:
        raise PermissionDenied('지울 권한이 없습니다.')

    else:
        post.delete()

    return redirect('posts:post-list')


def post_delete_bak(request, pk):

    if request.method == 'POST':
        post = get_object_or_404(Post, pk=pk)

        user = post.author

        if user != request.user:
            raise PermissionDenied('지울 권한이 없습니다.')

        else:
            post.delete()

    return redirect('posts:post-list')
