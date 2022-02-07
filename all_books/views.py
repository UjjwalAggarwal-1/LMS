from django.shortcuts import render
from .models import Books
from django.views.generic import ListView


def home(request):
    context = {'books': Books.objects.all()}
    return render(request, 'all_books/home.html', context)


class BookListView(ListView):
    model = Books
    template_name = 'all_books/home.html'
    context_object_name = 'books'
    # app/model_viewtype.html


def about(request):
    return render(request, 'all_books/about.html', {'title': 'about_view'})

