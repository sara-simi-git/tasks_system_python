from django import forms
from .models import *

class login(forms.Form):
    id = forms.IntegerField(label="Enter your Id", required=True)
    password = forms.CharField(label="Enter your password", max_length=10, required=True)


class register(forms.Form):
    id = forms.IntegerField(label="Enter your Id", required=True)
    fullName = forms.CharField(label="Enter your full name", max_length=20, required=True)
    password = forms.CharField(label="Enter your password", max_length=10, required=True)
    phone = forms.IntegerField(label="Enter your phone", required=True)
    team = forms.ModelChoiceField(label="Enter your team", queryset=Team.objects.all(), required=True)


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'description', 'finalDate']
