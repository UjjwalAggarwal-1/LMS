import datetime

from django import forms
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from .models import Books, Issue2
from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView, CreateView
from django.contrib import messages
from .forms import AddBookForm, RequestDecisionForm, RequestBookForm, ReturnBookForm
from django.contrib.auth.models import User


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
    model = Books
    template_name = 'all_books/home.html'
    context_object_name = 'books'
    ordering = ['-displayed_from']


def about(request):
    return render(request, 'all_books/about.html', {'title': 'about_view'})


class BookDetailView(DetailView):
    model = Books


def librarian_home(request):
    return render(request, 'all_books/librarian_home.html')


# def update_book(request):
#     if request.method == "POST":
#         form = UpdateBookForm(request.POST)#, initial={'title': instance.title})
#         if form.is_valid():
#             title = form.cleaned_data.get('title')
#             quantity = form.cleaned_data.get('quantity')
#             isbn = form.cleaned_data.get('isbn')
#             obj = all_books.models.Books.objects.get(isbn=isbn)
#             obj.title = title
#             obj.quantity = quantity
#             obj.save()
#             messages.success(request, 'updated successfully')
#             return redirect('librarian_home')
#     else:
#         form = UpdateBookForm()
#         return render(request, 'all_books/update_book.html', {'form': form})


class BookUpdateView(UpdateView):
    model = Books
    fields = ['isbn', 'title', 'quantity']
    template_name = 'all_books/update_book.html'
    success_url = reverse_lazy('librarian_home')


# class BookRequest(CreateView):
#     model = Issue2
#     fields = ['isbn_of_book', 'return_on']
#     template_name = 'all_books/request_book.html'
#
#     def get_initial(self, *args, **kwargs):
#         initial = super(BookRequest, self).get_initial(**kwargs)
#         #initial['isbn_of_book'] = Issue2.objects.get(id=self.request)
#         initial['student_id'] = self.request.user.username
#         return initial


def book_request(request, pk):
    if request.method == 'POST':
        form = RequestBookForm(request.POST, pk)
        if form.is_valid():
            return_on = form.cleaned_data.get('return_on')
            student_name = request.user.username
            book_object = Books.objects.get(pk=pk)
            student_object = User.objects.get(username=student_name)
            issue_inst = Issue2(isbn_of_book=book_object, student=student_object, return_on=return_on)
            issue_inst.save()
            messages.success(request, 'book was requested, please wait for approval')
            return redirect('all_books_home')
    else:
        form = RequestBookForm(initial={'return_on': datetime.date.today()+datetime.timedelta(days=20)})
    return render(request, 'all_books/request_book.html', {'form': form})


class IssueRequestListView(ListView):  # personal requests of the student!
    model = Issue2
    template_name = 'all_books/issue_requests.html'
    context_object_name = 'issue_requests_student'
    ordering = ['return_on']


def issue_request_listview(request):       # librarians page for viewing requests
    # if request.method == 'POST':
    #     form = RequestDecisionForm(request.POST)
    #     if form.is_valid():
    #         return redirect('librarian_home')
    # else:
    #     form = RequestDecisionForm()

    context_object = Issue2.objects.all()
    context = {'issue_requests': context_object}

    return render(request, 'all_books/librarian_home.html', context)


def issue_request_detailview(request, issue_request_id):
    if request.method == 'POST':
        form = RequestDecisionForm(request.POST, issue_request_id)
        if form.is_valid():
            issue_req_stat = form.cleaned_data.get('issue_request_status')
            reject_request_data = form.cleaned_data.get('reject_request')
            if (issue_req_stat and reject_request_data) or not(issue_req_stat and reject_request_data):
                raise forms.ValidationError(
                    "Please fill either reject reason or issue request status, but not both"
                )
            else:
                old_obj = Issue2.objects.get(id=issue_request_id)
                old_obj.issue_request_status = issue_req_stat
                old_obj.reject_request = reject_request_data
                old_obj.save()
                if issue_req_stat:
                    book = old_obj.isbn_of_book
                    book.quantity -= 1
                    book.save()
                return redirect('librarian_home')
    else:
        form = RequestDecisionForm()

    context = {'form': form, 'object': Issue2.objects.get(id=issue_request_id)}

    return render(request, 'all_books/librarian_home_2.html', context)


def cover(request):
    return render(request, 'all_books/cover.html', {'title': 'cover_page'})


# class ReturnBook(UpdateView):
#     model = Issue2
#     fields = ["issue_request_status"]
#     template_name = 'all_books/return_book.html'
#     success_url = reverse_lazy('issue_requests')


def return_book(request, pk):
    if request.method == 'POST':
        form = ReturnBookForm(request.POST, pk)
        if form.is_valid():
            issue_req_stat = form.cleaned_data.get('issue_request_status')
            old_obj = Issue2.objects.get(pk=pk)
            if not issue_req_stat:
                old_obj.issue_request_status = issue_req_stat
                old_obj.save()
                book = old_obj.isbn_of_book
                book.quantity += 1
                book.save()
            return redirect('issue_requests')
    else:
        form = ReturnBookForm()
    return render(request, 'all_books/return_book.html', {'form': form})
