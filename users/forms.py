from django import forms
from .models import Profile
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    user_name = forms.CharField(
        label='UserName',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'last_name','email' , 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)

class UpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['user_name', 'last_name', 'age', 'email', 'website', 'birth_day', 'PhoneNumber', 'location',
                  'about_me',
                  'birthPlace', 'status', 'gender', 'image', 'background_image']
