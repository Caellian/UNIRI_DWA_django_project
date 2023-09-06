
from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.utils.translation import gettext as _

class ProjectScheduleWidget(forms.MultiWidget):
    def __init__(self,*args,**kwargs) -> None:
        widgets = [
            forms.DateInput(attrs={'type': 'date'}),
            forms.DateInput(attrs={'type': 'date'}),
        ]
        super(ProjectScheduleWidget, self).__init__(widgets, *args,**kwargs)

    
    def decompress(self, value):
        if isinstance(value, ProjectSchedule):
            return [value.start_date, value.end_date]
        return [None, None]

    def format_output(self, rendered_widgets):
        return '<br>'.join(rendered_widgets)


class ProjectScheduleField(forms.MultiValueField):
    def __init__(self, *args, **kwargs):
        fields = [
            forms.DateField(),
            forms.DateField()
        ]
        super(ProjectScheduleField, self).__init__(fields, widget=ProjectScheduleWidget(), *args, **kwargs)

    def compress(self, data_list):
        if data_list:
            return ProjectSchedule(start_date=data_list[0], end_date=data_list[1], is_active=True)
        return None

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

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

class ProjectForm(forms.ModelForm):
    namespace = forms.CharField(max_length=32)
    name = forms.CharField(max_length=64)
    description = forms.CharField(widget=forms.Textarea)

    team = forms.ModelChoiceField(queryset=Team.objects.all())
    schedule = ProjectScheduleField()

    class Meta:
        model = Project
        fields = ['namespace', 'name', 'description', 'team', 'schedule']
