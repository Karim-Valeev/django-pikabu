from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Comment
from .models import Post
from .models.user import User


class AuthForm(forms.Form):
    email = forms.CharField(label="Email")
    password = forms.CharField(label="Password")


class RegForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


class PostForm(forms.ModelForm):
    title = forms.CharField(required=True, widget=forms.TextInput(attrs={"placeholder": "Enter title"}))
    body = forms.CharField(widget=forms.Textarea(attrs={"placeholder": "Write something :)"}))

    class Meta:
        model = Post
        fields = ["title", "body", "categories"]


class CommentForm(forms.ModelForm):
    text = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={"placeholder": "What do you think about this?", "autofocus": "true"}),
    )

    class Meta:
        model = Comment
        fields = ["text"]
