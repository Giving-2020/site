from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Count
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator

from blog.forms import BlogPostForm, CommentForm
from blog.models import BlogPost, DownVote, Upvote
from blog.utils import prepare_posts


class IndexView(View):
    template_name = 'blog/index.html'

    def get(self, request):
        posts = BlogPost.objects.order_by('-created_at')
        posts = prepare_posts(request, *posts)

        paginator = Paginator(posts, 2)
        page_obj = paginator.get_page(request.GET.get('page'))

        return render(request, self.template_name, {'is_paginated': True, 'page_obj': page_obj})


class HotPostsView(View):
    template_name = 'blog/hot_posts.html'

    def get(self, request):
        posts = BlogPost.objects.annotate(num_upvotes=Count('upvote')).order_by('-num_upvotes')
        posts = prepare_posts(request, *posts)

        paginator = Paginator(posts, 2)
        page_obj = paginator.get_page(request.GET.get('page'))

        return render(request, self.template_name, {'is_paginated': True, 'page_obj': page_obj})


user_member_required = user_passes_test(
    lambda user: user.is_staff or (user.groups.filter(name='Blog Writers').exists()),
    login_url='/')  # redirect to other path
decorators = [login_required, user_member_required]


@method_decorator(decorators, name='dispatch')
class CreatePostView(LoginRequiredMixin, View):
    template_name = 'blog/new_post.html'

    def get(self, request):
        form = BlogPostForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = BlogPostForm(request.POST)

        if not form.is_valid():
            messages.error(request, 'Invalid form', extra_tags='dnager')
            return render('create_post')

        post = form.save(commit=False)
        post.user = request.user
        post.save()

        return redirect('blog_post', post_id=post.id)


class BlogPostView(View):
    template_name = 'blog/blog_post.html'

    def get(self, request, post_id):
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

    def get(self, request, post_id):
        blog_post = get_object_or_404(BlogPost, id=post_id)
        return redirect('blog_post', post_id=post_id)

    def post(self, request, post_id):
        blog_post = get_object_or_404(BlogPost, id=post_id)

        form = CommentForm(request.POST)
        comment = form.save(commit=False)

        comment.blog_post = blog_post
        comment.user = request.user

        comment.save()

        return redirect('blog_post', post_id=post_id)


class UpdatePostView(LoginRequiredMixin, View):
    template_name = 'blog/update_post.html'

    def get(self, request, post_id):
        blog_post = get_object_or_404(BlogPost, id=post_id)

        if request.user != blog_post.user:
            return HttpResponseForbidden('You are not allowed to edit this post')

        form = BlogPostForm(instance=blog_post)
        return render(request, self.template_name, {'form': form, 'blog_post': blog_post})

    def post(self, request, post_id):
        blog_post = get_object_or_404(BlogPost, id=post_id)

        if request.user != blog_post.user:
            return HttpResponseForbidden('You are not allowed to edit this post')

        form = BlogPostForm(request.POST, instance=blog_post)
        form.save()

        messages.success(request, 'Post updated successfully')
        return redirect('blog_post', post_id=post_id)


class DeletePostView(LoginRequiredMixin, View):
    template_name = 'blog/delete_post.html'

    def get(self, request, post_id):
        blog_post = get_object_or_404(BlogPost, id=post_id)

        if request.user != blog_post.user:
            return HttpResponseForbidden('You are not allowed to delete this post')

        return render(request, self.template_name, {'blog_post': blog_post})

    def post(self, request, post_id):
        blog_post = get_object_or_404(BlogPost, id=post_id)

        if request.user != blog_post.user:
            return HttpResponseForbidden('You are not allowed to delete this post')

        blog_post.delete()
        return redirect('/')


class UpvoteView(LoginRequiredMixin, View):

    def get(self, request, post_id):
        return redirect(request.META.get('HTTP_REFERER', '/'))

    def post(self, request, post_id):
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

    def get(self, request, post_id):
        return redirect(request.META.get('HTTP_REFERER', '/'))

    def post(self, request, post_id):
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
