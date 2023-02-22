
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


class IssueForm(forms.Form):
    team = forms.ModelChoiceField(queryset=Team.objects.all())
    project = forms.ModelChoiceField(queryset=Project.objects.all())

    title = forms.CharField(max_length=128)
    description = forms.CharField(widget=forms.Textarea)

    status = forms.ChoiceField(choices=IssueStatus.choices)
    priority = forms.ChoiceField(choices=IssuePriority.choices)

    assigned = forms.ModelChoiceField(queryset=User.objects.all())

    def __init__(self, *args, **kwargs):
        self.request = None
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        
        super().__init__(*args, **kwargs)
        
    def clean(self):
        cleaned_data = super().clean()

        if self.request is not None:
            cleaned_data['author'] = self.request.user

        return cleaned_data

    def save(self):
        data = self.cleaned_data.cloned()
        data['project'] = Project.objects.filter(id=data['team']).first().id
        issue = Issue(*data)
        issue.save()
