from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
from members.exception import RelationNotExist, DuplicateRelationException


class User(AbstractUser):

    img_profile = models.ImageField(upload_to='user', blank=True)

    site = models.URLField(blank=True)

    introduction = models.TextField(blank=True)

    CHOICES_GENDER = (
        ('m', '남성'),
        ('f', '여성'),
        ('x', '선택안함'),
    )

    gender = models.CharField(max_length=1, choices=CHOICES_GENDER)

    to_relation_users = models.ManyToManyField(
        'self',
        through='Relation',
        symmetrical=False,
        blank=True,
        related_name='from_relation_users',
        related_query_name='from_relation_user',
    )

    def __str__(self):
        return self.username

    def follow(self, to_user):

        if self.relations_by_from_user.filter(to_user=to_user).exists():
            raise DuplicateRelationException(
                from_user=self,
                to_user=to_user,
                relation_type=Relation.RELATION_TYPE_FOLLOW,
            )
        return self.relations_by_from_user.create(
            to_user=to_user,
            relation_type=Relation.RELATION_TYPE_FOLLOW
        )

    def unfollow(self, to_user):

        q = self.relations_by_from_user.filter(
            to_user=to_user,
            relation_type=Relation.RELATION_TYPE_FOLLOW,
        )

        if q:
            q.delete()

        else:
            raise RelationNotExist(
                from_user=self,
                to_user=to_user,
                relation_type=Relation.RELATION_TYPE_FOLLOW,
            )

    @property
    def following(self):
        # 내가 팔로잉 중인 사람.
        # return User.objects.filter(
        #     pk__in=self.following_relations.values('to_user')
        # )

        return User.objects.filter(
            relations_by_to_user__from_user=self,
            relations_by_to_user__relation_type=Relation.RELATION_TYPE_FOLLOW
        )

    # 내가 팔로잉 하고 있는 사람 목록 중에 친구인 사람.
    # User.objects.filter(relations_by_to_user__from_user=self, relations_by_to_user__relation_type='f')

    @property
    def followers(self):
        # 나를 팔로잉 중인 사람.
        # return User.objects.filter(
        #     pk__in=self.follower_relations.values('from_user')
        # )
        return User.objects.filter(
            relations_by_from_user__to_user=self,
            relations_by_from_user__relation_type=Relation.RELATION_TYPE_FOLLOW
        )

    @property
    def block_user(self):
        # 나를 팔로잉 중인 사람.
        # return User.objects.filter(
        #     pk__in=self.block_relations.values('to_user')
        # )
        return User.objects.filter(
            relations_by_from_user__from_user=self,
            relations_by_to_user__relation_type=Relation.RELATION_TYPE_BLOCK
        )

    #  쿼리를 가져오는 프로퍼티들
    @property
    def following_relations(self):
        return self.relations_by_from_user.filter(
            relation_type=Relation.RELATION_TYPE_FOLLOW,
        )

    @property
    def follower_relations(self):
        return self.relations_by_to_user.filter(
            relation_type=Relation.RELATION_TYPE_FOLLOW,
        )

    @property
    def block_relations(self):
        return self.relations_by_from_user.filter(
            relation_type=Relation.RELATION_TYPE_BLOCK,
        )


class Relation(models.Model):
    """
    User 간의 MTM 연결 중계테이블
    """

    RELATION_TYPE_FOLLOW = 'f'
    RELATION_TYPE_BLOCK = 'b'

    CHOICES_RELATION_TYPE = (
        (RELATION_TYPE_FOLLOW, 'friend'),
        (RELATION_TYPE_BLOCK, 'block'),
    )

    # 팔로워 (친구 추가 요청자)
    from_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='relations_by_from_user',
    )

    # 팔로잉 할 대상 (친구 추가 대상)
    to_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='relations_by_to_user',
    )

    relation_type = models.CharField(
        max_length=1,
        choices=CHOICES_RELATION_TYPE
    )

    created_at = models.DateTimeField(auto_now_add=True)

    # 중복기능 제거
    class Meta:
        unique_together = (
            ('from_user', 'to_user'),
        )

    def __str__(self):
        return 'From {from_user} to {to_user} {type}'.format(
            from_user=self.from_user.username,
            to_user=self.to_user.username,
            type=self.get_relation_type_display(),
        )
