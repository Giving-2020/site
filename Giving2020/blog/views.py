import datetime

from blog.forms import AnnouncementForm, BlogPostForm, CommentForm
from blog.models import Announcement, BlogPost, DownVote, Upvote
from blog.utils import prepare_posts
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Count
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.views import View


def get_latest(obj):
    return sum(1 for a in obj if a.date.date() == datetime.datetime.now().date())


class IndexView(View):
    """Home Page View."""

    template_name = 'blog/index.html'

    def get(self, request):
        """Called upon a GET request."""
        posts = BlogPost.objects.order_by('-date')
        posts = prepare_posts(request, *posts)
        pt = get_latest(posts)
        at = get_latest(Announcement.objects.all().order_by('-date'))
        paginator = Paginator(posts, 2)
        page_obj = paginator.get_page(request.GET.get('page'))

        return render(request, self.template_name,
                      {'is_paginated': True, 'page_obj': page_obj, 'pt': pt, 'at': at})


class HotPostsView(View):
    """Hot Posts View."""

    template_name = 'blog/hot_posts.html'

    def get(self, request):
        """Called upon a GET request."""
        posts = BlogPost.objects.annotate(num_upvotes=Count('upvote')).order_by('-num_upvotes')
        posts = prepare_posts(request, *posts)

        paginator = Paginator(posts, 2)
        page_obj = paginator.get_page(request.GET.get('page'))
        pt = get_latest(BlogPost.objects.all().order_by('-date'))
        at = get_latest(Announcement.objects.all().order_by('-date'))
        return render(request, self.template_name,
                      {'is_paginated': True, 'page_obj': page_obj, 'pt': pt, 'at': at})


user_member_required = user_passes_test(
    lambda user: user.is_staff or (user.groups.filter(name='Blog Writers').exists()),
    login_url='/')  # redirect to other path
decorators = [login_required, user_member_required]


@method_decorator(decorators, name='dispatch')
class CreatePostView(LoginRequiredMixin, View):
    """Create New Post View."""

    template_name = 'blog/new_post.html'

    def get(self, request):
        """Called upon a GET request."""
        form = BlogPostForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        """Called upon a POST request."""
        form = BlogPostForm(request.POST)

        if not form.is_valid():
            messages.error(request, 'Invalid form', extra_tags='dnager')
            return render('create_post')

        post = form.save(commit=False)
        post.user = request.user
        post.save()
        messages.success(request, 'Posted successfully')
        return redirect('blog_post', post_id=post.id)


class BlogPostView(View):
    """View Blog Post View."""

    template_name = 'blog/blog_post.html'

    def get(self, request, post_id):
        """Called upon a GET request."""
        blog_post = get_object_or_404(BlogPost, id=post_id)
        blog_post = prepare_posts(request, blog_post)[0]

        comment_form = CommentForm()
        comments = blog_post.comment_set.all()

        context = {
            'blog_post': blog_post,
            'comment_form': comment_form,
            'comments': comments
        }

        return render(request, self.template_name, context)


class CommentView(LoginRequiredMixin, View):
    """Add New Coment View."""

    def get(self, request, post_id):
        """Called upon a GET request."""
        blog_post = get_object_or_404(BlogPost, id=post_id)
        return redirect('blog_post', post_id=post_id)

    def post(self, request, post_id):
        """Called upon a POST request."""
        blog_post = get_object_or_404(BlogPost, id=post_id)

        form = CommentForm(request.POST)
        comment = form.save(commit=False)

        comment.blog_post = blog_post
        comment.user = request.user

        comment.save()

        return redirect('blog_post', post_id=post_id)


class UpdatePostView(LoginRequiredMixin, View):
    """Update Blog Post View."""

    template_name = 'blog/update_post.html'

    def get(self, request, post_id):
        """Called upon a GET request."""
        blog_post = get_object_or_404(BlogPost, id=post_id)

        if request.user != blog_post.user:
            return HttpResponseForbidden('You are not allowed to edit this post')

        form = BlogPostForm(instance=blog_post)
        return render(request, self.template_name, {'form': form, 'blog_post': blog_post})

    def post(self, request, post_id):
        """Called upon a POST request."""
        blog_post = get_object_or_404(BlogPost, id=post_id)

        if request.user != blog_post.user:
            return HttpResponseForbidden('You are not allowed to edit this post')

        form = BlogPostForm(request.POST, instance=blog_post)
        form.save()

        messages.success(request, 'Post updated successfully')
        return redirect('blog_post', post_id=post_id)


class DeletePostView(LoginRequiredMixin, View):
    """Delete Blog Post View."""

    template_name = 'blog/delete_post.html'

    def get(self, request, post_id):
        """Called upon a GET request."""
        blog_post = get_object_or_404(BlogPost, id=post_id)

        if request.user != blog_post.user:
            return HttpResponseForbidden('You are not allowed to delete this post')

        return render(request, self.template_name, {'blog_post': blog_post})

    def post(self, request, post_id):
        """Called upon a POST request."""
        blog_post = get_object_or_404(BlogPost, id=post_id)

        if request.user != blog_post.user:
            return HttpResponseForbidden('You are not allowed to delete this post')

        blog_post.delete()
        return redirect('/')


class UpvoteView(LoginRequiredMixin, View):
    """User Upvote Blog View."""

    def get(self, request, post_id):
        """Called upon a GET request."""
        return redirect(request.META.get('HTTP_REFERER', '/'))

    def post(self, request, post_id):
        """Called upon a POST request."""
        blog_post = get_object_or_404(BlogPost, id=post_id)

        if any(post.user == request.user for post in blog_post.upvote_set.all()):
            upvote = blog_post.upvote_set.get(user=request.user)
            upvote.delete()
        else:
            upvote = Upvote.objects.create(blog_post=blog_post, user=request.user)
            upvote.save()

            if any(post.user == request.user for post in blog_post.downvote_set.all()):
                downvote = blog_post.downvote_set.get(user=request.user)
                downvote.delete()

        return redirect(request.META.get('HTTP_REFERER', '/'))


class DownVoteView(LoginRequiredMixin, View):
    """User Downvote Blog View."""

    def get(self, request, post_id):
        """Called upon a GET request."""
        return redirect(request.META.get('HTTP_REFERER', '/'))

    def post(self, request, post_id):
        """Called upon a POST request."""
        blog_post = get_object_or_404(BlogPost, id=post_id)

        if any(post.user == request.user for post in blog_post.downvote_set.all()):
            downvote = blog_post.downvote_set.get(user=request.user)
            downvote.delete()
        else:
            downvote = DownVote.objects.create(blog_post=blog_post, user=request.user)
            downvote.save()

            if any(post.user == request.user for post in blog_post.upvote_set.all()):
                upvote = blog_post.upvote_set.get(user=request.user)
                upvote.delete()

        return redirect(request.META.get('HTTP_REFERER', '/'))


class AnnouncementView(LoginRequiredMixin, View):
    """New Announcement View."""

    template_name = 'blog/announ.html'
    form_class = AnnouncementForm

    def get(self, request):
        """Called upon a GET request."""
        pt = get_latest(BlogPost.objects.all())
        at = get_latest(Announcement.objects.all().order_by('-date'))
        return render(request, self.template_name, {'form': self.form_class, 'at': at, 'pt': pt})

    def post(self, request):
        """Called upon a POST request."""
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Announcement Successful')
            return redirect('/announcements')

        return redirect(request.META.get('HTTP_REFERER', '/'))


class AllAnnouncementsView(LoginRequiredMixin, View):
    """All Announcements View."""

    template_name = 'blog/announcements.html'

    def get(self, request):
        """Called upon a GET request."""
        model = Announcement.objects.all().order_by('-date')
        pt = get_latest(BlogPost.objects.all().order_by('-date'))
        at = get_latest(Announcement.objects.all().order_by('-date'))

        return render(request, self.template_name, context={'a': model, 'pt': pt, 'at': at})


class SingleAnnouncementView(LoginRequiredMixin, View):
    """Single Announcement View."""

    model = Announcement
    template_name = 'blog/announcement.html'

    def get(self, request, pk):
        """Called upon a GET request."""
        pt = get_latest(BlogPost.objects.all())
        at = get_latest(Announcement.objects.all().order_by('-date'))
        return render(request, self.template_name,
                      context={'a': self.model.objects.get(id=pk), 'at': at, 'pt': pt})


class SuperUserView(LoginRequiredMixin, View):
    """Staff SuperUser View."""

    template_name = 'superview.html'

    def get(self, request):
        """Called upon a GET request."""
        users = User.objects.all().order_by('-date_joined')
        return render(request, self.template_name, context={'users': users})


class EditAnnouncementView(LoginRequiredMixin, View):
    """Edit Announcement View."""

    template_name = 'blog/announ.html'

    def get(self, request, pk):
        """Called upon a GET request."""
        ann = get_object_or_404(Announcement, id=pk)

        if request.user != ann.author:
            return HttpResponseForbidden('You are not authorized to edit this announcement.')

        form = AnnouncementForm(instance=ann)
        return render(request, self.template_name, {'form': form, 'ann': ann})

    def post(self, request, pk):
        """Called upon a POST request."""
        ann = get_object_or_404(Announcement, id=pk)

        if request.user != ann.author:
            return HttpResponseForbidden('You are noe authorized to edit this announcement.')

        form = AnnouncementForm(request.POST, instance=ann)
        form.save()

        messages.success(request, 'Announcement Updated successfully.')
        return redirect('announcements_single', pk=pk)


@login_required
def delete_user(request, pk):
    if request.user.is_superuser:
        user = User.objects.get(id=pk)
        user.delete()
        messages.warning(request, f'Deleted {user.username}.')
        return redirect('superuserview')
    else:
        return HttpResponseForbidden('Are you even supposed to be here?')


@login_required
def delete_announcement(request, pk):
    if request.method == 'POST':
        ann = Announcement.objects.get(id=pk)
        if request.user.is_staff and ann.author == request.user:
            ann.delete()
            messages.success(request, 'Announcement Deleted.')
            return redirect('announcements')
