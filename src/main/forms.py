from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models.user import User


class AuthForm(forms.Form):
    email = forms.CharField(label="Email")
    password = forms.CharField(label="Password")


class RegForm(UserCreationForm):
    # profile_pic = forms.ImageField(label="Аватарка", required=False)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
