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
from django.utils import timezone


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
    fields = ['title', 'author', 'publisher', 'published', 'isbn', 'quantity', 'genre', 'summary', 'location',
              'displayed_from']
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
        form = RequestBookForm(initial={'return_on': datetime.datetime.now() + datetime.timedelta(days=20)})
    return render(request, 'all_books/request_book.html', {'form': form})


class IssueRequestStudentListView(ListView):  # personal requests of the student!
    model = Issue
    template_name = 'all_books/issue_requests_student.html'
    context_object_name = 'issue_requests_student'


def issue_request_listview(request):  # for librarians' page for viewing requests
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
                reqbook = old_obj.isbn_of_book
                if issue_req_stat == 'issued':
                    reqbook.quantity -= 1
                    old_obj.issued_on = datetime.datetime.now()
                    reqbook.save()
                elif issue_req_stat == 'renewed':
                    old_obj.renewed_on = datetime.datetime.now()
                else:
                    old_obj.reject_request = reject_request_data
                old_obj.save()
                return redirect('librarian_home')
    else:
        form = RequestDecisionForm()

    reqbook = Issue.objects.get(id=issue_request_id).isbn_of_book
    reqstudent = Issue.objects.get(id=issue_request_id).student
    context = {'form': form, 'object': Issue.objects.get(id=issue_request_id),
               'studiss': Issue.objects.filter(student=reqstudent, isbn_of_book=reqbook,
                                               issue_request_status='issued').count()}

    return render(request, 'all_books/librarian_home_2.html', context)


def cover(request):
    lastmonth = timezone.now() - timezone.timedelta(days=30)
    trendissdict = {}

    for book in Book.objects.all():
        count = 0
        student_list = []
        for issobj in Issue.objects.filter(isbn_of_book=book):
            if issobj.issued_on >= lastmonth:
                if issobj.student not in student_list:
                    count += 1
                    student_list.append(issobj.student)
        trendissdict[book.title] = count

    trendisslist = []
    for i in range(3 if len(trendisslist) <= 3 else 12):
        maxcnt = max(trendissdict.values())
        maxiss = list(trendissdict.keys())[list(trendissdict.values()).index(maxcnt)]
        trendisslist.append(maxiss)
        trendissdict.pop(maxiss)

    context = {'title': 'cover_page',
               'new_arrivals': Book.objects.all()[:7:-1],
               'trending_issues': trendisslist}

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
            if (issue_req_stat == 'renewed' and renewed_request is None) or (
                    issue_req_stat == 'returned' and renewed_request is not None):
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


def more_search(request):
    genre_choice = ['Action', 'Adventure', 'Classics', 'Comic Book', 'Graphic Novel', 'Folklore', 'Detective',
                    'Horror', 'Literary Fiction', 'Romance', 'Science Fiction', 'Short Stories',
                    'Suspense', 'Thrillers', 'Biographies', 'Autobiographies', 'Cookbooks', 'History', 'Poetry',
                    'Mystery', 'Fantasy', 'Self Growth', 'True Crime']

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

    qs = Book.objects.all().order_by('title')

    if rtitle is not None:
        qs = qs.filter(title__icontains=rtitle)
    if risbn is not None:
        qs = qs.filter(isbn__icontains=risbn)
    if rauthor is not None:
        qs = qs.filter(author__icontains=rauthor)
    if rgenre is not None:
        qs = qs.filter(genre__icontains=rgenre)

    if rnotavailable:
        qs = qs.filter(quantity=0)
    if ravailable:
        qs = qs.exclude(quantity=0)

    if rdescorder:
        qs = qs.order_by('-published')
    if rascorder:
        qs = qs.order_by('published')

    if rpdate_min != '':
        qs = qs.filter(published__gte=rpdate_min)
    if rpdate_max != '':
        qs = qs.filter(published__lte=rpdate_max)
    if rddate_min != '':
        qs = qs.filter(displayed_from__gte=rddate_min)
    if rddate_max != '':
        qs = qs.filter(displayed_from__lte=rddate_max)

    context = {'genre': genre_choice, 'queryset': qs}

    return render(request, 'all_books/more_search.html', context)
