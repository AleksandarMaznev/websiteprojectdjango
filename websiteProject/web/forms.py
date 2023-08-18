from django import forms
from django.contrib.auth import authenticate as auth_authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator
from websiteProject.web.validators import TextAndNumsOnlyValidator


from .models import Profile, Book, Comment


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


class LoginForm(forms.Form):
    username = forms.CharField(
        label="username",
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'autofocus': True,

        })
    )
    password = forms.CharField(
        label="password",
        max_length=30,
        required=True,
        widget=forms.PasswordInput(attrs={
        }),
    )

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")

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


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content', 'posted_on']
        exclude= ['posted_on']

class EditCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

class EditBookForm(forms.ModelForm):
    cover = forms.FileField(widget=forms.FileInput)
    book_file = forms.FileField(widget=forms.FileInput)
    class Meta:
        model = Book
        fields = ['cover', 'book_file', 'synopsis']


class StaffSuperuserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    username = forms.CharField(required=True)
    password1 = forms.CharField(required=True, label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(required=True, label='Confirm Password', widget=forms.PasswordInput)

    user_type = forms.ChoiceField(choices=[('staff', 'Staff'), ('superuser', 'Superuser')])

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]

        if self.cleaned_data["user_type"] == "staff":
            user.is_staff = True
        elif self.cleaned_data["user_type"] == "superuser":
            user.is_staff = True
            user.is_superuser = True

        if commit:
            user.save()
        return user
