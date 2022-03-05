from django import forms
from all_books.models import Books, Issue2
import datetime


class UpdateBookForm(forms.Form):
    isbn = forms.CharField(max_length=20)
    title = forms.CharField(max_length=100)
    quantity = forms.IntegerField()


class RequestBookForm(forms.Form):
    now = datetime.date.today()
    return_on = forms.DateTimeField(widget=forms.SelectDateWidget(attrs={'min': now,
                                                                         'max': now + datetime.timedelta(days=20)}))


class AddBookForm(forms.ModelForm):
    class Meta:
        model = Books
        fields = ['title', 'isbn', 'quantity']


class RequestDecisionForm(forms.Form):
    issue_request_status = forms.BooleanField(required=False)
    reject_request = forms.CharField(max_length=300, required=False)


class ReturnBookForm(forms.ModelForm):
    class Meta:
        model = Issue2
        fields = ['issue_request_status']
        widgets = {'issue_reqeust_status': forms.ChoiceField(choices=(('ISSUED', 'YES'), ('NO', 'RETURNED'), ('UNKNOWN', 'UNKNOWN')))}


