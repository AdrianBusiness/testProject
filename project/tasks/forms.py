from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core import validators
from django import forms
from django.forms import ModelForm

from tasks.models import Task


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text='Required field', validators=[validators.validate_email])
    username = forms.CharField(required=False, widget=forms.HiddenInput)

    def __init__(self, *args, **kwargs):
        self.field_order = ['email', 'username', 'password1', 'password2']
        super(RegistrationForm, self).__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            if User.objects.filter(email=email).exists():
                raise forms.ValidationError('Email already exists')
        return email


class LoginForm(forms.Form):
    username = forms.CharField(max_length=50, min_length=3)
    password = forms.CharField(max_length=32, widget=forms.PasswordInput)


class TaskForm(ModelForm):
    user = forms.HiddenInput(attrs={'required': False})

    class Meta:
        model = Task
        exclude = ['opened', 'closed', 'completed', ]
