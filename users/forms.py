from django import forms

from users.models import Profile, User


class LoginForm(forms.Form):
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
    email = forms.EmailField(label='Email', max_length=32, widget=forms.TextInput(
        attrs={
            'placeholder': 'example@f1recloud.com'
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
    password2 = forms.CharField(label='Re-enter Password', max_length=32, widget=forms.PasswordInput(
        attrs={
            'placeholder': 'Password'
        }
    ))


class UpdateUserForm(forms.ModelForm):
    email = forms.EmailField(max_length=32)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


class UpdateProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['profile_picture', 'description']
