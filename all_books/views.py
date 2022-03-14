import datetime
import operator

from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import UpdateView, DeleteView

from .forms import AddBookForm, RejectRequestForm, RequestBookForm, RenewBookForm, ReturnBookForm, UpdateBookForm
from .models import Book, Issue, Genre


def add_book(request):
    if request.method == 'POST':
        form = AddBookForm(request.POST)
        if form.is_valid():
            if not Book.objects.filter(isbn=request.POST.get('isbn')):
                form.save()
                messages.success(request, 'added successfully')
                return redirect('librarian_controls')
            elif Book.objects.filter(isbn=request.POST.get('isbn')):
                form = AddBookForm()
                messages.warning(request, 'a book with same isbn was previously added')
                return render(request, 'all_books/add_book.html', {'form': form, 'title': 'ADD BOOK'})
    else:
        form = AddBookForm()
        return render(request, 'all_books/add_book.html', {'form': form, 'title': 'ADD BOOK'})


class DeleteBook(DeleteView):
    model = Book
    template_name = 'all_books/delete_book.html'
    success_url = reverse_lazy('librarian_controls')


class BookListView(ListView):
    model = Book
    template_name = 'all_books/home.html'
    context_object_name = 'books'
    ordering = ['-displayed_from']


def about(request):
    return render(request, 'all_books/about.html', {'title': 'ABOUT'})


def book_detail(request, pk):
    book_obj = Book.objects.get(pk=pk)
    issue_obj = Issue.objects.filter(book=book_obj)
    context = {'book_object': book_obj, 'issue_object': issue_obj, 'title': 'BOOK DETAIL'}
    return render(request, 'all_books/book_detail.html', context)


def librarian_controls(request):
    context = {'title': 'Controls',
               'pending_requests': Issue.objects.filter(status='pending'),
               'renewed_requests': Issue.objects.filter(status='renewed'),
               'returned_requests': Issue.objects.filter(status='returned'),
               }
    return render(request, 'all_books/librarian_controls.html', context)


class BookUpdateView(UpdateView):
    model = Book
    form_class = UpdateBookForm
    template_name = 'all_books/update_book.html'
    success_url = reverse_lazy('librarian_controls')


def book_request(request, pk):
    if request.method == 'POST':
        form = RequestBookForm(request.POST, pk)
        if form.is_valid():
            return_on = form.cleaned_data.get('return_on')
            book_object = Book.objects.get(pk=pk)
            student_object = request.user
            issue_inst = Issue.objects.create(book=book_object, student=student_object, return_on=return_on)
            messages.success(request, 'book was requested, please wait for approval')
            return redirect('all_books_home')
    else:
        form = RequestBookForm(initial={'return_on': datetime.datetime.now() + datetime.timedelta(days=20)})
    return render(request, 'all_books/request_book.html', {'form': form})


def issue_requests_student(request):  # personal requests of the student!
    io = Issue.objects
    context = {'pending_requests': io.filter(issue_request_status='pending').order_by('-requested_on', 'issued_on'),
               'issued_requests': io.filter(issue_request_status='issued').order_by('return_on', 'issued_on'),
               'returned_requests': io.filter(issue_request_status='returned').order_by('-returned_on', 'issued_on'),
               'rejected_requests': io.filter(issue_request_status='rejected').order_by('-requested_on'),
               'renewed_requests': io.filter(issue_request_status='renewed').order_by('-renewed_on', 'issued_on')}
    return render(request, 'all_books/issue_requests_student.html', context)


class DeleteMyRequest(DeleteView):
    model = Issue
    template_name = 'all_books/delete_book.html'
    success_url = reverse_lazy('issue_requests_student')


def all_request_listview(request):  # for librarians' page for viewing requests
    context_object = Issue.objects.all()
    context = {'all_issue_requests': context_object}

    return render(request, 'all_books/librarian_controls.html', context)


def request_decision(request, issue_request_id):
    reqbook = Issue.objects.get(id=issue_request_id).book
    reqstudent = Issue.objects.get(id=issue_request_id).student

    if request.method == 'POST':

        iss_obj = Issue.objects.get(id=issue_request_id)
        iss_obj.status = 'issued'
        iss_obj.issued_on = datetime.datetime.now()
        reqbook.quantity -= 1
        iss_obj.save()
        reqbook.save()
        return redirect('librarian_controls')

    context = {'object': Issue.objects.get(id=issue_request_id),
               'studiss': Issue.objects.filter(student=reqstudent, book=reqbook,
                                               issue_request_status='issued').count()}

    return render(request, 'all_books/request_decision.html', context)


def reject_request(request, issue_request_id):
    if request.method == 'POST':
        form = RejectRequestForm(request.POST, issue_request_id)
        if form.is_valid():
            iss_obj = Issue.objects.get(pk=issue_request_id)
            iss_obj.status = 'rejected'
            iss_obj.reject_request = form.cleaned_data.get('reject_reason')
            iss_obj.save()
            return redirect('librarian_controls')
    else:
        reject_form = RejectRequestForm()

    context = {'reject_form': reject_form}
    return render(request, 'all_books/reject_request.html', context)


def cover(request):
    qs = Book.objects.all()
    ordered_qs = sorted(qs, key=operator.attrgetter('unique_num_issues'))
    context = {'title': 'COVER',
               'new_arrivals': Book.objects.all().order_by('displayed_from')[::-1][:7],
               'trending_issues': ordered_qs[::-1][:6]}

    return render(request, 'all_books/cover.html', context)


def return_book(request, pk):
    if request.method == 'POST':
        form = ReturnBookForm(request.POST, pk)
        if form.is_valid():
            review = form.cleaned_data.get('review')
            rating = form.cleaned_data.get('rating')
            old_obj = Issue.objects.get(pk=pk)
            old_obj.status = 'returned'
            old_obj.returned_on = datetime.datetime.now()
            book = old_obj.book
            book.quantity += 1
            book.save()
            if review is not None:
                old_obj.review = review
            if rating is not None:
                old_obj.rating = rating
            old_obj.save()
            return redirect('issue_requests_student')
    else:
        form = ReturnBookForm()
    return render(request, 'all_books/return_book.html', {'form': form})


def renew_book(request, pk):
    if request.method == 'POST':
        form = RenewBookForm(request.POST, pk)
        if form.is_valid():
            old_obj = Issue.objects.get(pk=pk)
            old_obj.status = 'renewed'
            old_obj.returned_on = datetime.datetime.now()
            old_obj.save()
            return redirect('issue_requests_student')
        else:
            form = RenewBookForm()
            messages.warning(request, 'please fill out proper data')
    else:
        form = RenewBookForm()
    return render(request, 'all_books/return_book.html', {'form': form})


class ScoreTheReturn(UpdateView):
    model = Issue
    fields = ['score']
    template_name = 'all_books/score_return.html'
    success_url = reverse_lazy('librarian_controls')


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


def more_search(request):
    rtitle = request.GET.get('title')
    risbn = request.GET.get('isbn')
    rauthor = request.GET.get('author')
    rgenre = request.GET.get('genre')
    rddate_min = request.GET.get('ddate_min')
    rddate_max = request.GET.get('ddate_max')
    rpdate_min = request.GET.get('pdate_min')
    rpdate_max = request.GET.get('pdate_max')
    ravailable = request.GET.get('available')
    rnotavailable = request.GET.get('notavailable')
    rdescorder = request.GET.get('descorder')
    rascorder = request.GET.get('ascorder')
    rsummary = request.GET.get('summary')

    qs = Book.objects.all().order_by('title')

    if rtitle != '' and rtitle is not None:
        qs = qs.filter(title__icontains=rtitle)
    if risbn != '' and risbn is not None:
        qs = qs.filter(isbn=risbn)
    if rauthor != '' and rauthor is not None:
        qs = qs.filter(author__icontains=rauthor)
    if rgenre != '' and rgenre is not None:
        qs = qs.filter(genre=rgenre)
    if rsummary != '' and rsummary is not None:
        qs = qs.filter(summary__icontains=rsummary)

    if rnotavailable:
        qs = qs.filter(quantity=0)
    if ravailable:
        qs = qs.exclude(quantity=0)

    if rdescorder:
        qs = qs.order_by('-published')
    if rascorder:
        qs = qs.order_by('published')

    if rpdate_min != '' and rpdate_min is not None:
        qs = qs.filter(published__gte=rpdate_min)
    if rpdate_max != '' and rpdate_max is not None:
        qs = qs.filter(published__lte=rpdate_max)
    if rddate_min != '' and rddate_min is not None:
        qs = qs.filter(displayed_from__gte=rddate_min)
    if rddate_max != '' and rddate_max is not None:
        qs = qs.filter(displayed_from__lte=rddate_max)

    context = {'genre': Genre.objects.all(), 'queryset': qs, 'title': 'SEARCH'}

    return render(request, 'all_books/more_search.html', context)

