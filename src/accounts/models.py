from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    rating = models.PositiveSmallIntegerField(null=True, default=0)
    image = models.ImageField(null=True, default='default.jpg', upload_to='pics')
