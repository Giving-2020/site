from django.db import models
from markdownx.models import MarkdownxField
# from ckeditor.fields import RichTextField


class BlogPost(models.Model):
    """Model For Posting A Blog."""

    title = models.CharField(max_length=64)
    content = MarkdownxField()

    date = models.DateTimeField(auto_now_add=True)
    last_edited = models.DateTimeField(auto_now=True)

    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Upvote(models.Model):
    """Model For Upvote On Blog."""

    blog_post = models.ForeignKey('BlogPost', on_delete=models.CASCADE)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class DownVote(models.Model):
    """Model For Downvote On Blog."""

    blog_post = models.ForeignKey('BlogPost', on_delete=models.CASCADE)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    """Model For Commenting On A Blog."""

    content = models.TextField(max_length=4096)

    created_at = models.DateTimeField(auto_now_add=True)
    last_edited = models.DateTimeField(auto_now=True)

    blog_post = models.ForeignKey('BlogPost', on_delete=models.CASCADE)
    user = models.ForeignKey('auth.User', related_name='comments', on_delete=models.CASCADE)


class Announcement(models.Model):
    """Announcement Model."""

    title = models.CharField(max_length=1024)
    content = MarkdownxField()
    date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    def __str__(self):
        return self.title
