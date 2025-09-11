from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

# class AuthenticationForm(BaseAuthenticationForm):
#     class Meta:
#         model = BaseAuthenticationForm.Meta.model
#         fields = ['username', 'password']
        
    
