from django.shortcuts import redirect

from posts.models import Post


def comment_delete(request, post_pk, comment_pk):

    if request.method == 'POST':
        post = Post.objects.get(pk=post_pk)

        comment = post.comments.get(pk=comment_pk)

        print('댓글작성자', comment.username)
        print('삭제요청자', request.user.username)

        #
        if comment.username == request.user.username:
            print('이름 같음 ')
            comment.delete()

    return redirect('posts:post-detail', post_pk)