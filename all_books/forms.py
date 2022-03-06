import datetime
from django import forms
from all_books.models import Books, Issue2


class UpdateBookForm(forms.Form):
    isbn = forms.CharField(max_length=20)
    title = forms.CharField(max_length=100)
    quantity = forms.IntegerField()


class RequestBookForm(forms.ModelForm):
    class Meta:
        now = datetime.date.today()
        model = Issue2
        fields = ['return_on']
        widgets = {'return_on': forms.widgets.DateInput(attrs={'type': 'date', 'min': now, 'max': now + datetime.timedelta(days=20)})}


# class RequestBookForm(forms.Form):
#     now = datetime.date.today()
#     return_on = forms.DateField(widget=forms.SelectDateWidget(attrs={'min': now, 'max': now + datetime.timedelta(days=20)}))


class AddBookForm(forms.ModelForm):
    class Meta:
        model = Books
        fields = ['title', 'isbn', 'quantity']


class RequestDecisionForm(forms.Form):
    issue_request_status = forms.ChoiceField(choices=[
         ('issued', 'Approve request'), ('rejected', 'Reject')
    ], required=False)
    reject_request = forms.CharField(max_length=300, required=False)


class ReturnBookForm(forms.Form):
    issue_request_status = forms.ChoiceField(choices=[('returned', 'Return')])
