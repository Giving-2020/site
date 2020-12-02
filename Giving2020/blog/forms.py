from django import forms

from blog.models import BlogPost, Comment


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
