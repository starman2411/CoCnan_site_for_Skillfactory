from django.db import models
from django.contrib.auth.models import AbstractUser

# class CustomUser(AbstractUser):
#     pass
#
#     def __str__(self):
#         return self.username

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
