import uuid

from django.contrib.auth.models import Group
from django.db.models.signals import post_save, pre_delete, post_delete
from django.dispatch import receiver
from rest_framework_simplejwt.tokens import AccessToken

from accounts.models import User
from quiz.models import Result


@receiver(post_save, sender=Result)
def save_profile(sender, instance, created, **kwargs):
    if created:
        instance.user.rating += instance.points()
        instance.user.save(update_fields=['rating'])
