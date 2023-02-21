
from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.utils.translation import gettext as _

# UserCreationForm doesn't use get_user_model()
class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username",)
        field_classes = {"username": UsernameField}


class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ('namespace', 'name')
