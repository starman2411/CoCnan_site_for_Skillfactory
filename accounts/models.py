from django.db import models


class RegistrationCodes(models.Model):
    username = models.TextField(default='')
    email = models.EmailField(default='')
    code = models.TextField()
    creation_time = models.DateTimeField(auto_now_add=True)
