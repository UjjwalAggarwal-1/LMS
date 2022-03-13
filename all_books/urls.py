from django.urls import path
from users.views import login_redirect_view
from . import views
from .views import BookListView, book_detail, book_request, return_book, search, more_search, DeleteBook,\
    DeleteMyRequest, renew_book

urlpatterns = [
    path('', BookListView.as_view(), name='all_books_home'),
    path('randomloremIsem1/', login_redirect_view, name='login_then?'),
    path('about/', views.about, name='all_books_about'),
    path('<int:pk>/', book_detail, name='book_detail'),
    path('issue_requests_student/', views.IssueRequestStudentListView.as_view(), name='issue_requests_student'),
    path('update_book/<int:pk>/', views.BookUpdateView.as_view(), name='update_book'),
    path('book_request/<int:pk>/', book_request, name='book_request'),
    path('return_book/<int:pk>/', return_book, name='return_book'),
    path('renew_book/<int:pk>/', renew_book, name='renew_book'),
    path('score_return/<int:pk>/', views.ScoreTheReturn.as_view(), name='score_return'),
    path('search/', search, name='search'),
    path('more_search/', more_search, name='more_search'),
    path('<int:pk>/delete_book/', DeleteBook.as_view(), name='delete_book'),
    path('<int:pk>/delete_my_request/', DeleteMyRequest.as_view(), name='delete_my_request'),
]
