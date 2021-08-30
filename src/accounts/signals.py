import uuid

from django.db.models.signals import post_save
from django.dispatch import receiver

from accounts.models import User


@receiver(post_save, sender=User)
def save_profile(sender, instance, created, **kwargs):
    from accounts import roles
    if created:
        instance.groups.add(roles.USERS)
        instance.tg_auth_token = uuid.uuid4()
        instance.save()
