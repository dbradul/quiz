from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from accounts.models import User

# Create your models here.

class Test(models.Model):
    QUESTION_MIN_LIMIT = 3
    QUESTION_MAX_LIMIT = 20

    class LEVEL_CHOICES(models.IntegerChoices):
        BASIC = 0, "Basic"
        MIDDLE = 1, "Middle"
        ADVANCED = 2, "Advanced"

    # topic = models.ForeignKey(to=Topic, related_name='tests', null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=64)
    description = models.TextField(max_length=1024, null=True, blank=True)
    level = models.PositiveSmallIntegerField(choices=LEVEL_CHOICES.choices, default=LEVEL_CHOICES.MIDDLE)
    image = models.ImageField(default='default.png', upload_to='covers')

    def __str__(self):
        return f'{self.title}'


class Question(models.Model):
    ANSWER_MIN_LIMIT = 3
    ANSWER_MAX_LIMIT = 6

    test = models.ForeignKey(to=Test, related_name='questions', on_delete=models.CASCADE)
    order_number = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(Test.QUESTION_MIN_LIMIT),
                    MaxValueValidator(Test.QUESTION_MAX_LIMIT)])
    text = models.CharField(max_length=64)

    def __str__(self):
        return f'{self.text}'


class Choice(models.Model):
    text = models.CharField(max_length=64)
    question = models.ForeignKey(to=Question, related_name='answers', on_delete=models.CASCADE)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.text}'


class Result(models.Model):
    class STATE(models.IntegerChoices):
        NEW = 0, "New"
        FINISHED = 1, "Finished"

    user = models.ForeignKey(to=User, related_name='results', on_delete=models.CASCADE)
    test = models.ForeignKey(to=Test, related_name='results', on_delete=models.CASCADE)
    state = models.PositiveSmallIntegerField(default=STATE.NEW, choices=STATE.choices)


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