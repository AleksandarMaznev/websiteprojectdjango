from django import forms
from django.contrib.auth import authenticate as auth_authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator
from websiteProject.web.validators import TextAndNumsOnlyValidator


from .models import Profile, Book


# Create your forms here.

class UserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

    # def clean(self):
    #     super().clean()
    #
    #     # Check if the username is unique
    #     if Profile.objects.filter(username=self.cleaned_data['username']).exists():
    #         raise forms.ValidationError(
    #             ['Username already exists. Please choose a different username.'])
    #
    #     # Check if the email is unique
    #     if Profile.objects.filter(email=self.cleaned_data['email']).exists():
    #         raise forms.ValidationError(
    #             ['Email already exists. Please choose a different email address.'])
    #
    #     return self.cleaned_data


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


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'genre', 'synopsis', 'cover', 'book_file', 'posted_on']
        exclude = ['author', 'posted_on']