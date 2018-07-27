from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.test import TestCase, TransactionTestCase

# Create your tests here.
from members.exception import RelationNotExist, DuplicateRelationException
from posts.models import Post, Comment
from posts.models.comment_like import CommentLike

User = get_user_model()


# class RelationTestCase(TransactionTestCase):
#
#     def create_dummy_user(self, num):
#
#         return [User.objects.create_user(username=f'u{x + 1}') for x in range(num)]
#
#
#     def test_follow(self):
#
#         u1, u2 = self.create_dummy_user(2)
#
#         u1.follow(u2)
#
#     def test_follow_only_one(self):
#
#         u1, u2 = self.create_dummy_user(2)
#
#         u1.follow(u2)
#
#         try:
#             u1.follow(u2)
#         except DuplicateRelationException:
#             print('이미 팔로우 되어 있습니다.')
#
#         with self.assertRaises(DuplicateRelationException):
#             u1.follow(u2)
#
#         self.assertEqual(u1.following.count(), 1)
#
#         # relation = u1.relations_by_from_user.create(to_user=u2, relation_type='f')
#
#         # print(User.objects.filter(pk=u2.pk).exists())
#
#         # u1 의 following에 u2가 포함되어있는지 확인
#         # print('1번 확인')
#         # self.assertIn(u2, u1.following)
#         #
#         # # u1 의 following_relation 에서 to_user 가 u2인 relation
#         # # self.following_relations.filter(to_user=u2).exists()
#         # print('2번 확인', self.assertTrue(u1.following_relations.filter(to_user=u2).exists()))
#         #
#         # # relation이 u1.following_relatons에 포함되어 있는지
#         # self.assertIn(relation, u1.following_relations)
#
#     def test_unfollow_only_follow_exist(self):
#
#         u1, u2 = self.create_dummy_user(2)
#
#         # u1 이 u2 를 언팔로우
#         u1.follow(u2)
#
#         u1.unfollow(u2)
#
#         self.assertNotIn(u2, u1.following)
#
#     def test_unfollow_fail_if_follow_not_exist(self):
#         u1, u2 = self.create_dummy_user(2)
#
#         with self.assertRaises(RelationNotExist):
#             u1.unfollow(u2)


