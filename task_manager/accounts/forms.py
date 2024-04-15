from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
    
class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'w-full px-3 py-2 rounded-lg bg-gray-700 text-gray-300 outline-none focus-within:ring-1 focus-within:ring-offset-blue-900'
        }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'w-full px-3 py-2 rounded-lg bg-gray-700 text-gray-300 outline-none focus-within:ring-1 focus-within:ring-offset-blue-900 mb-6'
        }))
    