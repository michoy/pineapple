# coding=utf-8
""" This is where forms for the about module are stored """
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.models import Group

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if username == '':
            raise forms.ValidationError('Username field empty. Please try again.')
        if not user or not user.is_active:
            raise forms.ValidationError("Sorry, that login was invalid. Please try again.")
        return self.cleaned_data

    def login(self, request):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        return user

class RegisterForm(forms.Form):
    username = forms.CharField(max_length=150, required=True)
    email = forms.CharField(max_length=150, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput, required=True)

    def clean(self):
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Sorry, that username is already taken. Please try again.")
        if password != confirm_password:
            raise forms.ValidationError("Sorry, your passwords don't match. Please try again.")
        return self.cleaned_data

    def register(self):
        group = Group.objects.get(name='Student')
        stud = User.objects.create_user(
            username=self.cleaned_data.get('username'),
            email=self.cleaned_data.get('email'),
            password=self.cleaned_data.get('password')
        )
        stud.groups.add(group)
