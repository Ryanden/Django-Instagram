from django.shortcuts import redirect, render

from posts.models import Comment, Post


def comment_like(request, post_pk, comment_pk):

    if request.method == 'POST':

        post = Post.objects.get(pk=post_pk)

        comment = Comment.objects.get(pk=comment_pk)

        print(comment)
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
