from django.core.validators import MaxValueValidator
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    class Meta:
        permissions = [('view_stats', 'View statistics')]

    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    rating = models.PositiveSmallIntegerField(null=True, default=0, validators=[MaxValueValidator(100)])
    image = models.ImageField(null=True, default='default.jpg', upload_to='pics')
    tg_auth_token = models.UUIDField(null=True, blank=True)

    # def save(self, *args, **kwargs):
    #     print(self.full_clean())
    #     super().save(*args, **kwargs)
