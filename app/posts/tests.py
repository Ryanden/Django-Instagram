from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.test import TestCase, TransactionTestCase

from posts.models import Post, Comment
from posts.models.comment_like import CommentLike

User = get_user_model()


class PostTestCase(TransactionTestCase):

    def create_dummy_user(self, num):

        return [User.objects.create_user(username=f"u{x + 1}") for x in range(num)]

    def test_comment_like(self):

        # 유저가 하트버튼을 눌러 각 코멘트마다 좋아요 할 수 있도록 함

        u1, u2 = self.create_dummy_user(2)

        p1 = Post.objects.create(author=u1)

        c1 = Comment.objects.create(post=p1, user=u1, content='1번코멘트')

        # cl1 = CommentLike.objects.create(user=u2, comment=c1)
        #
        # comment_info = Comment.objects.get(pk=p1.pk)
        #
        # comment_like_info = CommentLike.objects.get(pk=u2.pk)
        #
        # print('코멘트 : ', comment_info)
        # print('코멘트 좋아요 : ', comment_like_info)

        print('테스트코드')


    #
    # def test_follow_only_one(self):
    #
    #     u1, u2 = self.create_dummy_user(2)
    #
    #     u1.follow(u2)
    #
    #     try:
    #         u1.follow(u2)
    #     except DuplicateRelationException:
    #         print('이미 팔로우 되어 있습니다.')
    #
    #     with self.assertRaises(DuplicateRelationException):
    #         u1.follow(u2)
    #
    #     self.assertEqual(u1.following.count(), 1)
    #
    #     relation = u1.relations_by_from_user.create(to_user=u2, relation_type='f')
    #
    #     print(User.objects.filter(pk=u2.pk).exists())
    #
    #     u1 의 following에 u2가 포함되어있는지 확인
    #     print('1번 확인')
    #     self.assertIn(u2, u1.following)
    #
    #     # u1 의 following_relation 에서 to_user 가 u2인 relation
    #     # self.following_relations.filter(to_user=u2).exists()
    #     print('2번 확인', self.assertTrue(u1.following_relations.filter(to_user=u2).exists()))
    #
    #     # relation이 u1.following_relatons에 포함되어 있는지
    #     self.assertIn(relation, u1.following_relations)
    #
    # def test_unfollow_only_follow_exist(self):
    #
    #     u1, u2 = self.create_dummy_user(2)
    #
    #     # u1 이 u2 를 언팔로우
    #     u1.follow(u2)
    #
    #     u1.unfollow(u2)
    #
    #     self.assertNotIn(u2, u1.following)
    #
    # def test_unfollow_fail_if_follow_not_exist(self):
    #     u1, u2 = self.create_dummy_user(2)
    #
    #     with self.assertRaises(RelationNotExist):
    #         u1.unfollow(u2)
