from django import forms
from django.contrib.auth.models import User
from .models import Profile


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