import datetime
from django import forms
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from .models import Book, Issue
from django.views.generic import ListView
from django.views.generic.edit import UpdateView
from .forms import AddBookForm, RequestDecisionForm, RequestBookForm, ReturnBookForm


def add_book(request):
    if request.method == 'POST':
        form = AddBookForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'added successfully')
            return redirect('librarian_home')
    else:
        form = AddBookForm()
        return render(request, 'all_books/add_book.html', {'form': form})


class BookListView(ListView):
    model = Book
    template_name = 'all_books/home.html'
    context_object_name = 'books'
    ordering = ['-displayed_from']


def about(request):
    return render(request, 'all_books/about.html', {'title': 'about_view'})


def BookDetailView(request, pk):
    book_obj = Book.objects.get(pk=pk)
    issue_obj = Issue.objects.filter(isbn_of_book=book_obj)
    context = {'book_object': book_obj, 'issue_object': issue_obj}
    return render(request, 'all_books/book_detail.html', context)


def librarian_home(request):
    return render(request, 'all_books/librarian_home.html')


class BookUpdateView(UpdateView):
    model = Book
    fields = ['isbn', 'title', 'quantity']
    template_name = 'all_books/update_book.html'
    success_url = reverse_lazy('librarian_home')


def book_request(request, pk):
    if request.method == 'POST':
        form = RequestBookForm(request.POST, pk)
        if form.is_valid():
            return_on = form.cleaned_data.get('return_on')
            student_name = request.user.username
            book_object = Book.objects.get(pk=pk)
            student_object = User.objects.get(username=student_name)
            issue_inst = Issue(isbn_of_book=book_object, student=student_object, return_on=return_on)
            issue_inst.save()
            messages.success(request, 'book was requested, please wait for approval')
            return redirect('all_books_home')
    else:
        form = RequestBookForm(initial={'return_on': datetime.datetime.now()+datetime.timedelta(days=20)})
    return render(request, 'all_books/request_book.html', {'form': form})


class IssueRequestStudentListView(ListView):  # personal requests of the student!
    model = Issue
    template_name = 'all_books/issue_requests_student.html'
    context_object_name = 'issue_requests_student'


def issue_request_listview(request):       # for librarians' page for viewing requests
    context_object = Issue.objects.all()
    context = {'all_issue_requests': context_object}

    return render(request, 'all_books/librarian_home.html', context)


def issue_request_detailview(request, issue_request_id):
    if request.method == 'POST':
        form = RequestDecisionForm(request.POST, issue_request_id)
        if form.is_valid():
            issue_req_stat = form.cleaned_data.get('issue_request_status')
            reject_request_data = form.cleaned_data.get('reject_request')
            condtn = (reject_request_data == '')
            if (issue_req_stat in {'issued', 'renewed'} and not condtn) or (issue_req_stat == 'rejected' and condtn):
                raise forms.ValidationError("Please fill either reject reason or issue request status, but not both")
            else:
                old_obj = Issue.objects.get(id=issue_request_id)
                old_obj.issue_request_status = issue_req_stat
                book = old_obj.isbn_of_book
                if issue_req_stat == 'issued':
                    book.quantity -= 1
                    old_obj.issued_on = datetime.datetime.now()
                    book.save()
                elif issue_req_stat == 'renewed':
                    old_obj.renewed_on = datetime.datetime.now()
                else:
                    old_obj.reject_request = reject_request_data
                old_obj.save()
                return redirect('librarian_home')
    else:
        form = RequestDecisionForm()

    stu_iss_qs = Issue.objects.filter(student=Issue.objects.get(id=issue_request_id).student)
    tscore = 0
    tcount = stu_iss_qs.count()

    for data in stu_iss_qs:
        tscore += data.score
        if data.score == 0:
            tcount -= 1
    merit_score = tscore / tcount
    merit_score = round(merit_score, 3)
    context = {'form': form, 'object': Issue.objects.get(id=issue_request_id), 'mets': merit_score}

    return render(request, 'all_books/librarian_home_2.html', context)


def cover(request):
    last_month = datetime.datetime.now() - datetime.timedelta(days=30)
    context = {'title': 'cover_page',
               'new_arrivals': Book.objects.all()[:7:-1],
               'trending_issues': Issue.objects.values('isbn_of_book_id').distinct()}

    return render(request, 'all_books/cover.html', context)


def return_book(request, pk):
    if request.method == 'POST':
        form = ReturnBookForm(request.POST, pk)
        if form.is_valid():
            issue_req_stat = form.cleaned_data.get('issue_request_status')
            renewed_request = form.cleaned_data.get('request_renewal_till')
            review = form.cleaned_data.get('review')
            rating = form.cleaned_data.get('rating')
            old_obj = Issue.objects.get(pk=pk)
            old_obj.issue_request_status = issue_req_stat
            if (issue_req_stat == 'renewed' and renewed_request is None) or (issue_req_stat == 'returned' and renewed_request is not None):
                raise forms.ValidationError("invalid combination of data")
            else:
                if issue_req_stat == 'returned':
                    old_obj.returned_on = datetime.datetime.now()
                    book = old_obj.isbn_of_book
                    book.quantity += 1
                    book.save()
                elif issue_req_stat == 'renewed':
                    old_obj.return_on = renewed_request
                if review is not None:
                    old_obj.review = review
                if rating is not None:
                    old_obj.rating = rating
            old_obj.save()
            return redirect('issue_requests_student')
    else:
        form = ReturnBookForm()
    return render(request, 'all_books/return_book.html', {'form': form})


class ScoreTheReturn(UpdateView):
    model = Issue
    fields = ['score']
    template_name = 'all_books/score_return.html'
    success_url = reverse_lazy('librarian_home')


def search(request):
    query = request.GET['query']
    if query == '':
        context = {}
    else:
        context = {
            'book_objs_title': Book.objects.filter(title__icontains=query),
            'book_objs_author': Book.objects.filter(author__icontains=query),
            'book_objs_isbn': Book.objects.filter(isbn__icontains=query),
            'query': query,
                   }
    return render(request, 'all_books/search_results.html', context)