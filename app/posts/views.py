from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseNotAllowed
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.views.decorators.http import require_POST

from posts.forms import PostForm, PostModelForm
from posts.models.post_like import PostLike
from posts.models.comment_like import CommentLike

from .models.post import Post
from .models.comment import Comment


def post_list(request):

    posts = Post.objects.all()

    context = {
        'post_list': posts
    }

    return render(request, 'posts/post_list.html', context)


def post_detail(request, pk):

    post = Post.objects.get(pk=pk)

    context = {
        'post': post
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


def post_like(request, pk):

    if request.method == 'POST':

        print('라이크')
        post = Post.objects.get(pk=pk)

        PostLike.objects.create(
            user=request.user,
            post=post
        )

        return redirect('posts:post-list')

    return render(request, 'posts/post_list.html')


def comment_create(request, pk):

    if request.method == 'POST':

        post = Post.objects.get(pk=pk)

        Comment.objects.create(
            post=post,
            user=request.user,
            content=request.POST.get('comment')
        )

        return redirect('posts:post-detail', post.pk)

    return render(request, 'posts/post_detail.html')


def comment_delete(request, post_pk, comment_pk):

    if request.method == 'POST':
        post = Post.objects.get(pk=post_pk)

        comment = post.comments.get(pk=comment_pk)

        if comment.user == request.user:
            comment.delete()

    return redirect('posts:post-detail', post_pk)


def comment_like(request, post_pk, comment_pk):

    if request.method == 'POST':

        post = Post.objects.get(pk=post_pk)

        comment = Comment.objects.get(pk=comment_pk)

        # # commentlike 를 요청한 유저와 현재 유저의 비교
        # if request.user.commentlike_user == request.user:
        #
        #     print('아직 좋아요하지 않음')
        #
        #     # 좋아요를 하지 않았고 좋아요가 없으면 좋아요함
        #     if not request.user.commentlike_user:
        #         CommentLike.objects.create(
        #             user=request.user,
        #             comment=comment,
        #         )
        #
        # else:

        return redirect('posts:post-detail', post_pk)

    return render(request, 'posts/post_detail', post_pk)


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


def post_delete_bak(request, pk):

    if request.method == 'POST':
        post = get_object_or_404(Post, pk=pk)

        user = post.author

        if user != request.user:
            raise PermissionDenied('지울 권한이 없습니다.')

        else:
            post.delete()

    return redirect('posts:post-list')
