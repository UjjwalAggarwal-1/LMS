import os
import xlrd
import datetime
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LMS.settings')
django.setup()

from all_books.models import Book, Genre

path = 'C:\\Users\\HP\\Desktop\\Book1.xls'
workbook = xlrd.open_workbook(path)
worksheet = workbook.sheet_by_index(0)
n_rows = worksheet.nrows
n_cols = worksheet.ncols

for row in range(1, n_rows):
    new_book = Book.objects.create(
        title='d', isbn=0, author='d', publisher='d', location='d', quantity=0, summary='d'
    )
    for col in range(n_cols):
        data = worksheet.cell_value(row, col)
        if col == 0:
            new_book.isbn = data
        elif col == 1:
            new_book.title = data
        elif col == 2:
            genre_list = data.split(", ")
            for genre in genre_list:
                genre = Genre.objects.get_or_create(name__iexact=genre)
                genre = genre[0].id
                new_book.genre.add(genre)
        elif col == 3:
            new_book.author = data
        elif col == 4:
            new_book.publisher = data
        elif col == 5:
            data = xlrd.xldate_as_tuple(data, workbook.datemode)
            data = datetime.datetime(*data)
            new_book.published = data
        elif col == 6:
            data = xlrd.xldate_as_tuple(data, workbook.datemode)
            data = datetime.datetime(*data)
            new_book.displayed_from = data
        elif col == 7:
            new_book.location = data
        elif col == 8:
            new_book.quantity = data
        elif col == 9:
            new_book.summary = data
        new_book.save()





