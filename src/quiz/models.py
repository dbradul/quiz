from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from accounts.models import User

# Create your models here.
from core.models import BaseModel
from core.utils import generate_uuid


class Test(BaseModel):
    QUESTION_MIN_LIMIT = 3
    QUESTION_MAX_LIMIT = 20

    class LEVEL_CHOICES(models.IntegerChoices):
        BASIC = 0, "Basic"
        MIDDLE = 1, "Middle"
        ADVANCED = 2, "Advanced"

    # topic = models.ForeignKey(to=Topic, related_name='tests', null=True, on_delete=models.SET_NULL)
    uuid = models.UUIDField(default=generate_uuid, db_index=True, unique=True)
    title = models.CharField(max_length=64)
    description = models.TextField(max_length=1024, null=True, blank=True)
    level = models.PositiveSmallIntegerField(choices=LEVEL_CHOICES.choices, default=LEVEL_CHOICES.MIDDLE)
    image = models.ImageField(default='default.png', upload_to='covers')

    def questions_count(self):
        return self.questions.count()

    def get_best_result(self):
        return 42

    def __str__(self):
        return f'{self.title}'


class Question(models.Model):
    ANSWER_MIN_LIMIT = 3
    ANSWER_MAX_LIMIT = 6

    test = models.ForeignKey(to=Test, related_name='questions', on_delete=models.CASCADE)
    order_number = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(Test.QUESTION_MAX_LIMIT)])
    text = models.CharField(max_length=64)

    def __str__(self):
        return f'{self.text}'


class Choice(models.Model):
    text = models.CharField(max_length=64)
    question = models.ForeignKey(to=Question, related_name='choices', on_delete=models.CASCADE)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.text}'


class Result(BaseModel):
    class STATE(models.IntegerChoices):
        NEW = 0, "New"
        FINISHED = 1, "Finished"

    user = models.ForeignKey(to=User, related_name='results', on_delete=models.CASCADE)
    test = models.ForeignKey(to=Test, related_name='results', on_delete=models.CASCADE)
    state = models.PositiveSmallIntegerField(default=STATE.NEW, choices=STATE.choices) # TODO: derive from current_order_number
    uuid = models.UUIDField(default=generate_uuid, db_index=True, unique=True)
    current_order_number = models.PositiveSmallIntegerField(null=True)

    num_correct_answers = models.PositiveSmallIntegerField(
        default=0,
        validators=[
            MaxValueValidator(Test.QUESTION_MAX_LIMIT)
        ]
    )
    num_incorrect_answers = models.PositiveSmallIntegerField(
        default=0,
        validators=[
            MaxValueValidator(Test.QUESTION_MAX_LIMIT)
        ]
    )

    def update_result(self, order_number, selected_choices):
        question = Question.objects.filter(test=self.test, order_number=order_number).first()
        choices = [q.id for q in question.choices.filter(is_correct=True)]

        correct_answer = choices.sort() == selected_choices.sort()

        self.num_correct_answers += int(correct_answer)
        self.num_incorrect_answers += 1 - int(correct_answer)
        self.current_order_number = order_number

        if order_number == question.test.questions_count():
            self.state = self.STATE.FINISHED
            self.user.rating += self.points()
            self.user.save()

        self.save()

    def points(self):
        return max(0, self.num_correct_answers - self.num_incorrect_answers)
