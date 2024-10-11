from django import forms
from .models import Post, Comment

# blog/forms.py
from django import forms
from .models import Post,Reply

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'image', 'video']  # Include image and video fields

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['author', 'content']


class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['content']