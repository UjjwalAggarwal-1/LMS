from django.urls import path
from . import views
from .views import BookListView


urlpatterns = [
    path('', BookListView.as_view(), name='all_books_home'),
    path('about/', views.about, name='all_books_about')
]
