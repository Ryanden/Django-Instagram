from django.shortcuts import redirect, render

from posts.models import Post, PostLike


def post_like(request, pk):

    if request.method == 'POST':

        print('라이크')
        post = Post.objects.get(pk=pk)

        likeuser = post.postlike_postname.filter(user=request.user)

        if likeuser:

            likeuser.delete()

        else:
            print('중복유저 없음 만듬')
            PostLike.objects.create(
                user=request.user,
                post=post
            )

        return redirect('posts:post-list')

    return render(request, 'posts/post_list.html')