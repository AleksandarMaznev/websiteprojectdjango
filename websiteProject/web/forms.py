from django import forms
from django.contrib.auth import authenticate
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

        # def __init__(self, *args, **kwargs):
        #     super().__init__(*args, **kwargs)
        #     for field in self.fields:
        #         self.fields[field].required = True


class LoginForm(forms.Form):
    username = forms.CharField(
        label="Username",
        max_length=30,
        required=True,
    )
    password = forms.CharField(
        label="Password",
        max_length=30,
        required=True,
        widget=forms.PasswordInput(),
    )

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")

        user = authenticate(username=username, password=password)

        if user is None:
            raise forms.ValidationError("Incorrect username or password")

        return cleaned_data
