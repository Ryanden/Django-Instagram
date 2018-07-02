from .post_create import *
from .post_like import *
from .post_delete import *
from .post_detail import *
from .post_list import *
from .comment_like import *
from .comment_create import *
from .comment_delete import *

# @login_required()
# def post_create_with_form(request):
#
#     if request.method == 'POST':
#
#         form = PostForm(request.POST, request.FILES)
#
#         if form.is_valid():
#
#             print('유효함')
#
#             post = form.upload_file(request.user)
#
#             return redirect('posts:post-detail', pk=post.pk)
#
#     else:
#
#         if not request.user.is_authenticated:
#             return redirect('members:login')
#
#         form = PostForm()
#     context = {
#         'form': form,
#     }
#     return render(request, 'posts/post_create.html', context)
#
#
# def post_delete_bak(request, pk):
#
#     if request.method == 'POST':
#         post = get_object_or_404(Post, pk=pk)
#
#         user = post.author
#
#         if user != request.user:
#             raise PermissionDenied('지울 권한이 없습니다.')
#
#         else:
#             post.delete()
#
#     return redirect('posts:post-list')
