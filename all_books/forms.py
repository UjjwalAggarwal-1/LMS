import datetime
import django.forms
from django import forms
from all_books.models import Book, Issue


class RequestBookForm(forms.ModelForm):
    class Meta:
        now = datetime.date.today()
        twenty_days = datetime.timedelta(days=20)
        model = Issue
        fields = ['return_on']
        widgets = {'return_on': forms.widgets.DateInput(attrs={'type': 'date', 'min': now, 'max': now + twenty_days})}


class AddBookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'
        exclude = ('availability',)
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Title ...'}),
            'isbn': forms.TextInput(attrs={'placeholder': 'ISBN ...'}),
            'author': forms.TextInput(attrs={'placeholder': 'Author ...'}),
            'summary': forms.Textarea(attrs={'placeholder': 'Enter summary here'}),
            'displayed_from': forms.widgets.DateInput(attrs={'type': 'date', 'min': datetime.date.today()}),
            'published': forms.widgets.DateInput(attrs={'type': 'date'}),
            'genre': forms.CheckboxSelectMultiple()
        }


class UpdateBookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'
        exclude = ('availability',)
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Title ...'}),
            'isbn': forms.TextInput(attrs={'placeholder': 'ISBN ...'}),
            'author': forms.TextInput(attrs={'placeholder': 'Author ...'}),
            'summary': forms.Textarea(attrs={'placeholder': 'Enter summary here'}),
            'displayed_from': forms.widgets.DateInput(attrs={'type': 'date', 'min': datetime.date.today()}),
            'published': forms.widgets.DateInput(attrs={'type': 'date'}),
            'genre': forms.CheckboxSelectMultiple()
        }


class RejectRequestForm(forms.Form):
    reject_reason = forms.CharField(max_length=300)


class RenewRequestDecisionForm(forms.Form):
    issue_request_status = forms.ChoiceField(choices=[
        ('renewed', 'Renew Request'), ('rejected', 'Reject')
    ])
    reject_request = forms.CharField(max_length=300, required=False)


class ReturnBookForm(forms.Form):
    rating = forms.ChoiceField(choices=[(0, 'No Rating'), (1, 'Poor'), (2, 'Average'),
                                        (3, 'Good'), (4, 'Very Good'), (5, 'Excellent')],
                               required=False)
    review = forms.CharField(widget=forms.Textarea(), required=False)


class RenewBookForm(forms.Form):
    now = datetime.date.today()
    twenty_days = datetime.timedelta(days=20)
    request_renewal_till = forms.DateField(widget=django.forms.DateInput(attrs=
                                                                         {'type': 'date', 'min': now,
                                                                          'max': now + twenty_days}),
                                           required=False)
