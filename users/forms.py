# forms.py içinde olmalı
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django import forms
from django.contrib.auth import authenticate
from django.utils.safestring import mark_safe


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'password1', 'password2', 'gender']
        # help_texts = {'email': 'We will never share your email.', 'gender': 'You must choose one'}

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError(
                mark_safe('This email is already registered. <a href="/users/login/">Wanna login?</a>')
            )
        return email
class EmailLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        user = authenticate(username=email, password=password)  
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            raise forms.ValidationError("Invalid email or password.")
        if not user.is_active:
            raise forms.ValidationError("Your account is not active. Please verify your email.")
        if user is None:
            raise forms.ValidationError("Invalid email or password")
        self.user = user
        return self.cleaned_data