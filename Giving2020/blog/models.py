from django.db import models
from markdownx.models import MarkdownxField

class BlogPost(models.Model):
    title = models.CharField(max_length=64)
    content = MarkdownxField(max_length=16384)

    created_at = models.DateTimeField(auto_now_add=True)
    last_edited = models.DateTimeField(auto_now=True)

    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)


class Upvote(models.Model):
    blog_post = models.ForeignKey('BlogPost', on_delete=models.CASCADE)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class DownVote(models.Model):
    blog_post = models.ForeignKey('BlogPost', on_delete=models.CASCADE)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    content = models.TextField(max_length=4096)

    created_at = models.DateTimeField(auto_now_add=True)
    last_edited = models.DateTimeField(auto_now=True)

    blog_post = models.ForeignKey('BlogPost', on_delete=models.CASCADE)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
