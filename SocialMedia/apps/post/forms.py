from django import forms
from apps.post.models.post import Comment, Post


class NewPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content', 'image', ]


class NewCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
