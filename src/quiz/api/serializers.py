from rest_framework import serializers

from accounts.models import User
from quiz.models import Test, Result, Question, Choice

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
    class Meta:
        model = Question
        fields = ('id', 'order_number', 'text')


class QuestionDetailSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ('id', 'order_number', 'text', 'choices')


class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = (
            'id',
            'title',
            'questions_count',
        )


class TestDetailSerializer(serializers.HyperlinkedModelSerializer):
    # questions = serializers.HyperlinkedRelatedField(
    #     view_name='api:test-question-detail', many=True, queryset=Question.objects.filter(order_number=1)
    # )
    questions = QuestionSerializer(many=True, read_only=True)
    # questions = serializers.PrimaryKeyRelatedField(many=True, queryset=Question.objects.all().order_by('order_number'))

    class Meta:
        model = Test
        fields = (
            'id',
            'title',
            # 'description',
            # 'level',
            'questions_count',
            'questions',
        )


class ResultSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    test = serializers.ReadOnlyField(source='test.id')
    questions_count = serializers.ReadOnlyField(source='test.questions_count')

    class Meta:
        model = Result
        fields = (
            'id',
            'test',
            'user',
            'state',
            'get_state_display',
            'current_order_number',
            'num_correct_answers',
            'num_incorrect_answers',
            'questions_count',
            'points',
        )


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username',
            'rating',
        )
