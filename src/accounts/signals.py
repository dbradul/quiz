from django.contrib.auth.models import Group
from django.db.models.signals import post_save, pre_delete, post_delete
from django.dispatch import receiver

from accounts import roles
from accounts.models import User


@receiver(post_save, sender=User)
def save_profile(sender, instance, created, **kwargs):
    if created:
        # instance.groups.add(Group.objects.get(name='Users'))
        instance.groups.add(roles.USERS)
