from django.shortcuts import render

# Create your views here.
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


