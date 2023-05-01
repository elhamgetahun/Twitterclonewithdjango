from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import  User, Post


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'password1', 'password2']





class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['avatar', 'name', 'username', 'email', 'bio',]




class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['content', 'image']
        