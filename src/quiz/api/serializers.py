from rest_framework import serializers

from accounts.models import User
from quiz.models import Test


class TestSerializer(serializers.ModelSerializer):

    class Meta:
        model = Test
        fields = (
            'id',
            'title',
            'description',
            'level',
        )


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username',
            'rating',
            # 'get_rating',
        )

