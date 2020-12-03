from django import forms

from blog.models import BlogPost, Comment, Announcement


class BlogPostForm(forms.ModelForm):

    class Meta:
        model = BlogPost
        fields = ['title', 'content']


class CommentForm(forms.ModelForm):
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
    class Meta:
        model = Announcement
        fields = ('title', 'content', 'author')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title...'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Content'}),
            'author': forms.TextInput(attrs={'id': 'auth', 'type': 'hidden'})
        }