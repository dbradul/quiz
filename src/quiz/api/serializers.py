from rest_framework import serializers

from accounts.models import User
from quiz.models import Test, Result, Question, Choice


class TestSerializer(serializers.ModelSerializer):

    class Meta:
        model = Test
        fields = (
            'id',
            # 'uuid',
            'title',
            # 'description',
            # 'level',
            'questions_count',
        )


class ResultSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    test = serializers.ReadOnlyField(source='test.id')
    questions_count = serializers.ReadOnlyField(source='test.questions_count')

    class Meta:
        model = Result
        fields = (
            'id',
            # 'uuid',
            'test',
            'user',
            'state',
            'get_state_display',
            'current_order_number',
            'num_correct_answers',
            'num_incorrect_answers',
            'questions_count',
        )


class ChoiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Choice
        fields = (
            'id',
            'text',
            # 'test',
            'is_correct',
        )


class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = (
            'id',
            'order_number',
            'text',
            'choices'
        )


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username',
            'rating',
            # 'get_rating',
        )

