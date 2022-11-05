from django.db import models
from users.models import CustomUser
from django.contrib.postgres.fields import ArrayField


class Category(models.Model):
    category_name = models.TextField()

    def __str__(self):
        return self.category_name


class Post(models.Model):
    title = models.TextField()
    text = models.TextField()
    creation_time = models.DateTimeField(auto_now_add=True)
    attached_files = ArrayField(models.TextField(blank=True), size=3, default=list)

    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    category = models.ManyToManyField(Category, through='PostCategory', blank=True)


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Response(models.Model):
    text = models.TextField()
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    creation_time = models.DateTimeField(auto_now_add=True)
    is_confirmed = models.BooleanField(default=False)
