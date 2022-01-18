from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    mobile_number = forms.IntegerField()
    BITSID = forms.CharField()

    class Meta:
        model = User
        fields = ['username', 'email', 'BITSID', 'mobile_number', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    mobile_number = forms.IntegerField()
    BITSID = forms.CharField()

    class Meta:
        model = User
        fields = ['username', 'BITSID', 'mobile_number']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']
