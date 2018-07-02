from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from posts.models import Post


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
