from blog.models import Announcement, BlogPost, Comment
from django import forms


class BlogPostForm(forms.ModelForm):
    """Blog Post form."""

    class Meta:
        model = BlogPost
        fields = ['title', 'content']


class CommentForm(forms.ModelForm):
    """Blog Comment form."""

    content = forms.CharField(label='', widget=forms.Textarea(
        attrs={
            'placeholder': 'Comment here',
            'rows': 3
        }
    ))

    class Meta:
        model = Comment
        fields = ['content']


class AnnouncementForm(forms.ModelForm):
    """Announcement form."""

    class Meta:
        model = Announcement
        fields = ('title', 'content', 'author')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title...'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Content...'}),
            'author': forms.TextInput(attrs={'id': 'auth', 'type': 'hidden'})
        }
