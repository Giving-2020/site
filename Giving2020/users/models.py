from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    profile_picture = models.ImageField(default='default.png', upload_to='profile_pictures')

    description = models.TextField(max_length=4096, blank=True)
