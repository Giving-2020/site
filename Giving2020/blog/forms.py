from django import forms
from blog.models import BlogPost, Comment, Category

choice = Category.objects.all().values_list('name', 'name')
choice_list = []
for item in choice:
    choice_list.append(item)


class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'category', 'content']

        widgets = {
            'category': forms.Select(choices=choice_list, attrs={'class': 'form-control'})
        }


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
