# forms.py içinde olmalı
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django import forms
from django.contrib.auth import authenticate

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'password1', 'password2', 'gender']
        # help_texts = {'email': 'We will never share your email.','gender':'You must choose one'}
        
class EmailLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        user = authenticate(username=email, password=password)  # Yes, still use "username" param
        if user is None:
            raise forms.ValidationError("Invalid email or password")
        self.user = user
        return self.cleaned_data