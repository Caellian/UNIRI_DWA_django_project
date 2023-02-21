
from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField


class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username",)
        field_classes = {"username": UsernameField}


class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ("username",)
        field_classes = {"username": UsernameField}
