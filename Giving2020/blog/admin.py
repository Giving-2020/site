from django.contrib import admin

from blog.models import BlogPost, Comment, DownVote, Upvote, Announcement, Category


admin.site.register(BlogPost)
admin.site.register(Comment)
admin.site.register(DownVote)
admin.site.register(Upvote)
admin.site.register(Announcement)
admin.site.register(Category)