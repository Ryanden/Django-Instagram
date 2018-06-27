from django.shortcuts import render, redirect
from members.models import User

# Create your views here.
from posts.forms import PostForm
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

        form = PostForm(request.POST, request.FILES)

        if form.is_valid():

            print('유효함')

            form.upload_file(request.user)

            # file = Post(request.FILES['image'])

            return redirect('posts:post-list')

    else:

        if not request.user.is_authenticated:
            return redirect('members:login')

        form = PostForm()
    context = {
        'form': form,
    }
    return render(request, 'posts/post_create.html', context)


def post_delete(request, pk):

    if request.method == 'POST':

        post = Post.objects.get(id=pk)

        user = post.author

        print('현재유저:', request.user)
        print('글작성자:', user)

        print(request.user)

        if user == request.user:
            print('같은유저')

            post.delete()
        else:
            print('다른유저')

    return redirect('index')
