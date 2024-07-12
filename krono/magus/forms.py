from django import forms
from .models import Task

class StartTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['task_type']

class EndTaskForm(forms.Form):
    task_type = forms.CharField(max_length=100)
