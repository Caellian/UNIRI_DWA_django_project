
from django import forms
from .models import Project

class DateInput(forms.DateInput):
    input_type = 'date'

class ProjectCreateForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'start_date']
        widgets = {
            'start_date': DateInput()
        }
