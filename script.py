import os
import xlrd
import datetime
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LMS.settings')
django.setup()

from all_books.models import Book, Genre

folder = os.getcwd()
file_name = 'Book1.xls'
path = os.path.join(folder, file_name)
workbook = xlrd.open_workbook(path)
worksheet = workbook.sheet_by_index(0)
n_rows = worksheet.nrows
n_cols = worksheet.ncols

for row in range(1, n_rows):
    new_book = Book.objects.create(
        title='d', isbn=0, author='d', publisher='d', location='d', quantity=0, summary='d'
    )
    for col in range(n_cols):
        new_book.isbn = worksheet.cell_value(row, 0)
        new_book.title = worksheet.cell_value(row, 1)
        #  genre at bottom
        new_book.author = worksheet.cell_value(row, 3)
        new_book.publisher = worksheet.cell_value(row, 4)
        new_book.published = datetime.datetime(*(xlrd.xldate_as_tuple(worksheet.cell_value(row, 5), workbook.datemode)))
        new_book.displayed_from = datetime.datetime(*(xlrd.xldate_as_tuple(worksheet.cell_value(row, 6), workbook.datemode)))
        new_book.location = worksheet.cell_value(row, 7)
        new_book.quantity = worksheet.cell_value(row, 8)
        new_book.summary = worksheet.cell_value(row, 9)
        #  for genre
        genre_list = (worksheet.cell_value(row, 2)).split(", ")
        for genre in genre_list:
            genre = Genre.objects.get_or_create(name__iexact=genre)
            genre = genre[0].id
            new_book.genre.add(genre)

        new_book.save()