from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User

        fields = (
            'pk',
            'username',
            'img_profile',
            'site',
            'introduction',
            'gender',
            'to_relation_users',
            'last_name',
            'first_name',
        )

