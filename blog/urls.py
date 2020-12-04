from django.urls import path
import random
import secrets
from blog.views import (
    BlogPostView,
    CommentView,
    CreatePostView,
    DeletePostView,
    DownVoteView,
    HotPostsView,
    IndexView,
    UpdatePostView,
    UpvoteView,
    AnnouncementView,
    SingleAnnouncementView,
    AllAnnouncementsView,
    SuperUserView,
    delete_user,
    
)


key = secrets.token_hex(78)

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('hot_posts/', HotPostsView.as_view(), name='hot_posts'),
    path('post/create/', CreatePostView.as_view(), name='create_post'),
    path('post/<int:post_id>/', BlogPostView.as_view(), name='blog_post'),
    path('post/<int:post_id>/update/', UpdatePostView.as_view(), name='update_post'),
    path('post/<int:post_id>/delete/', DeletePostView.as_view(), name='delete_post'),
    path('post/<int:post_id>/upvote/', UpvoteView.as_view(), name='upvote_post'),
    path('post/<int:post_id>/downvote/', DownVoteView.as_view(), name='downvote_post'),
    path('post/<int:post_id>/comment/', CommentView.as_view(), name='comment_post'),
    path('announcement/', AnnouncementView.as_view(), name='announcement'),
    path('announcements/<int:pk>', SingleAnnouncementView.as_view(), name='announcements_single'),
    path('announcements/', AllAnnouncementsView.as_view(), name='announcements'),
    path(f'superuser/{key}', SuperUserView.as_view(), name='superuserview'),
    path(f'user/delete/{key}/<int:pk>', delete_user, name='delete_user'),
]
