from django import forms
from .models import Profile


class StuProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bits_id', 'mobile_num', 'hostel', 'room_no']


class LibProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['mobile_num', 'image']
