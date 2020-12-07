from blog.models import Announcement, BlogPost, Comment, DownVote, Upvote
from django.contrib import admin

admin.site.register((BlogPost, Comment, DownVote, Upvote, Announcement))
