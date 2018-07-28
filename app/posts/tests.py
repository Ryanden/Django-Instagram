import json
import random

from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.test import TestCase, TransactionTestCase
from rest_framework import status
from rest_framework.test import APITestCase

from posts.models import Post, Comment
from posts.models.comment_like import CommentLike

User = get_user_model()


#
# class PostTestCase(TransactionTestCase):
#
#     def create_dummy_user(self, num):
#         return [User.objects.create_user(username=f"u{x + 1}") for x in range(num)]
#
#     def test_comment_like(self):
#         # 유저가 하트버튼을 눌러 각 코멘트마다 좋아요 할 수 있도록 함
#
#         u1, u2 = self.create_dummy_user(2)
#
#         p1 = Post.objects.create(author=u1)
#
#         c1 = Comment.objects.create(post=p1, user=u1, content='1번코멘트')
#
#         # cl1 = CommentLike.objects.create(user=u2, comment=c1)
#         #
#         # comment_info = Comment.objects.get(pk=p1.pk)
#         #
#         # comment_like_info = CommentLike.objects.get(pk=u2.pk)
#         #
#         # print('코멘트 : ', comment_info)
#         # print('코멘트 좋아요 : ', comment_like_info)
#
#         print('테스트코드')


def get_dummy_user():
    return User.objects.create_user(
        username='dummy',
        password='123',
        gender='m'
    )


def get_dummy_post(author):
    return [Post.objects.create(author=author, content=f'{content}') for content in range(random.randint(1, 10))]


class PostListTest(APITestCase):
    URL = '/api/posts/'

    CREATE_URL = '/api/posts/create/'

    def test_post_list_status_code(self):
        response = self.client.get(self.URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_list_count(self):
        author = get_dummy_user()
        get_dummy_post(author)

        response = self.client.get(self.CREATE_URL)
        data = json.loads(response.content)

        # print(data)

        self.assertEqual(len(data), Post.objects.count())

    def test_post_list_order_by_create_descending(self):
        author = get_dummy_user()
        posts = get_dummy_post(author)

        post_list = []
        for item in posts:
            post_list.append(item.pk)

        self.assertEqual(post_list, list(Post.objects.order_by('created_at').values_list('pk', flat=True)))


    def test_post_create(self):
        self