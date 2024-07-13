from django import forms
from .models import Task
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class StartTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['task_type']

class EndTaskForm(forms.Form):
    task_type = forms.CharField(max_length=100)

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

