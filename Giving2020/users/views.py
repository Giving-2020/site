from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from blog.models import BlogPost
from blog.utils import prepare_posts
from users.forms import LoginForm, RegisterForm, UpdateProfileForm, UpdateUserForm
from users.models import User


class ProfileView(View):
    template_name = 'users/profile.html'

    def get(self, request, user_id=None):
        if user_id is None and request.user.is_authenticated:
            return redirect('profile', user_id=request.user.id)

        user = get_object_or_404(User, id=user_id)

        posts = BlogPost.objects.filter(user=user).order_by('-created_at')
        posts = prepare_posts(request, *posts)

        paginator = Paginator(posts, 2)
        page_obj = paginator.get_page(request.GET.get('page'))

        context = {
            'is_paginated': True,
            'page_obj': page_obj,
            'user_query': user
        }

        return render(request, self.template_name, context)


class LoginView(View):
    template_name = 'users/login.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('/')

        form = LoginForm()
        request.session['next'] = request.GET.get('next')
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        if request.user.is_authenticated:
            return redirect('/')

        form = LoginForm(request.POST)

        if not form.is_valid():
            messages.error(request, 'Invalid form', extra_tags='danger')
            return redirect('login')

        user = authenticate(
            request,
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password']
        )

        if user is not None:
            login(request, user)

            redirect_url = request.session.get('next')
            request.session['next'] = None

            messages.success(request, 'Login successful')

            return redirect(redirect_url or '/')

        messages.error(request, 'Invalid username or password', extra_tags='danger')
        return redirect('login')


class UpdateProfileView(LoginRequiredMixin, View):
    template_name = 'users/update_profile.html'

    def get(self, request):
        context = {
            'user_form': UpdateUserForm(instance=request.user),
            'profile_form': UpdateProfileForm(instance=request.user.profile)
        }
        return render(request, self.template_name, context)

    def post(self, request):
        user_form = UpdateUserForm(
            request.POST,
            instance=request.user
        )
        profile_form = UpdateProfileForm(
            request.POST,
            request.FILES,
            instance=request.user.profile
        )

        if not user_form.is_valid() or not profile_form.is_valid():
            messages.error(request, 'Invalid form', extra_tags='danger')
            return redirect('update_profile')

        user_form.save()
        profile_form.save()

        messages.success(request, 'Your profile has been successfully updated')
        return redirect('profile')


class RegisterView(View):
    template_name = 'users/register.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('/')

        form = RegisterForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        if request.user.is_authenticated:
            return redirect('/')

        form = RegisterForm(request.POST)

        error = False

        if not form.is_valid():
            messages.error(request, 'Invalid form', extra_tags='danger')
            error = True

        else:
            if form.cleaned_data['password1'] != form.cleaned_data['password2']:
                messages.error(request, 'Passwords do not match', extra_tags='danger')
                error = True

            if len(User.objects.filter(username=form.cleaned_data['username'])) > 0:
                messages.error(request, 'Username already exists', extra_tags='danger')
                error = True

            if len(User.objects.filter(email=form.cleaned_data['email'])) > 0:
                messages.error(request, 'Email already in use', extra_tags='danger')
                error = True

        if error:
            return redirect('register')

        user = User(
            email=form.cleaned_data['email'],
            username=form.cleaned_data['username']
        )
        user.set_password(form.cleaned_data['password1'])
        user.save()

        messages.success(request, 'Registration successful')

        return redirect('login')
