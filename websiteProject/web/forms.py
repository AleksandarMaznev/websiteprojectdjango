from django import forms
from django.contrib.auth import authenticate as auth_authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Book


# Create your forms here.

class ProfileModelForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['username', 'email', 'password']
        widgets = {
            'username': forms.TextInput(attrs={
                'placeholder': 'Username'
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'Email'
            }),
            'password': forms.PasswordInput(attrs={
                'placeholder': 'Password'
            })

        }


class LoginForm(forms.Form):
    username = forms.CharField(
        label="username",
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
                'placeholder': 'Username'
            })
    )
    password = forms.CharField(
        label="password",
        max_length=30,
        required=True,
        widget=forms.PasswordInput(attrs={
                'placeholder': 'Password'
            }),
    )

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")
        print(username + " " + password)

        user = auth_authenticate(username=username, password=password)
        print(user)

        if user is None:
            raise forms.ValidationError("Incorrect username or password")

        return cleaned_data
