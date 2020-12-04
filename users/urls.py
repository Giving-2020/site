from django.contrib.auth.views import LogoutView, PasswordResetConfirmView, PasswordResetCompleteView, PasswordResetDoneView, PasswordResetView
from django.urls import path

from users.views import LoginView, ProfileView, RegisterView, UpdateProfileView


urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('password-reset/', PasswordResetView.as_view(template_name='users/password_reset.html'), name='password_reset'),
    path('password-reset/done/', PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/', PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'), name='password_reset_complete'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/<int:user_id>/', ProfileView.as_view(), name='profile'),
    path('update_profile/', UpdateProfileView.as_view(), name='update_profile')
]
