import datetime
import random
import time

from celery import shared_task

from accounts.models import User
from quiz.models import Result


@shared_task
def mine_bitcoin(n):
    time.sleep(random.randint(1, n))



@shared_task
def normalize_phones(filter):
    qs = User.objects.filter(**filter)
    if qs:
        for user in qs:
            print('Processed', user.username)
            user.save()
    else:
        print('Qs is empty')


@shared_task
def cleanup_outdated_results():
    outdated_tests = Result.objects.filter(
        state=Result.STATE.NEW,
        write_date__lte=datetime.datetime.now() - datetime.timedelta(seconds=7*24*3600)
    )
    outdated_tests.delete()

    print('Outdated results deleted!')
