from django.db import models
from markdownx.models import MarkdownxField
from ckeditor.fields import RichTextField
class BlogPost(models.Model):
    title = models.CharField(max_length=64)
    content = RichTextField(max_length=16384)

    date = models.DateTimeField(auto_now_add=True)
    last_edited = models.DateTimeField(auto_now=True)

    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

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
    user = models.ForeignKey('auth.User',related_name='comments', on_delete=models.CASCADE)

class Announcement(models.Model):
    title = models.CharField(max_length=1024)
    content = RichTextField()
    date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    def __str__(self):
        return self.title