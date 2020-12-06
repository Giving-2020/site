from django import forms
from users.models import Profile, User


class LoginForm(forms.Form):
    """Account Login form, to collect username and password."""

    username = forms.CharField(label='Username', max_length=32, widget=forms.TextInput(
        attrs={
            'placeholder': 'Username'
        }
    ))
    password = forms.CharField(label='Password', max_length=32, widget=forms.PasswordInput(
        attrs={
            'placeholder': 'Password'
        }
    ))


class RegisterForm(forms.Form):
    """Account registration form, to collect email, username, password and password confirmation."""

    email = forms.EmailField(label='Email', max_length=32, widget=forms.TextInput(
        attrs={
            'placeholder': 'example@giving2020.com'
        }
    ))
    username = forms.CharField(label='Username', max_length=32, widget=forms.TextInput(
        attrs={
            'placeholder': 'Username'
        }
    ))

    password1 = forms.CharField(label='Password', max_length=32, widget=forms.PasswordInput(
        attrs={
            'placeholder': 'Password'
        }
    ))
    password2 = forms.CharField(label='Re-enter Password', max_length=32,
                                widget=forms.PasswordInput(
                                    attrs={
                                        'placeholder': 'Password'
                                    }
                                ))


class UpdateUserForm(forms.ModelForm):
    """Account updating form, to collect email, username, name."""

    email = forms.EmailField(max_length=32)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


class UpdateProfileForm(forms.ModelForm):
    """Profile updating form, to collect profile picture and description."""

    class Meta:
        model = Profile
        fields = ['profile_picture', 'description']
