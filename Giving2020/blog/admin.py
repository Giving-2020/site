from django.contrib import admin

from blog.models import BlogPost, Comment, DownVote, Upvote, Announcement


admin.site.register((BlogPost,Comment,DownVote,Upvote,Announcement))