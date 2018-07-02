from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from django.views.decorators.http import require_POST

from posts.models import Post, Comment


@login_required
@require_POST
def comment_create(request, post_pk, comment_pk=None):

    post = get_object_or_404(Post, pk=post_pk)

    parent_comment = get_object_or_404(Comment, pk=comment_pk) if comment_pk else None

    post.comments.create(
        _author=request.user,
        _content=request.POST.get('comment')
    )

    return redirect('posts:post-detail', post.pk)







