from django.urls import path
from users.views import login_redirect_view
from . import views
from .views import BookListView, BookDetailView, book_request, return_book

urlpatterns = [
    path('', BookListView.as_view(), name='all_books_home'),
    path('randomloremIsem1/', login_redirect_view, name='login_then?'),
    path('about/', views.about, name='all_books_about'),
    path('<int:pk>/', BookDetailView, name='book_detail'),
    path('issue_requests_student/', views.IssueRequestStudentListView.as_view(), name='issue_requests_student'),
    path('update_book/<int:pk>/', views.BookUpdateView.as_view(), name='update_book'),
    path('book_request/<int:pk>/', book_request, name='book_request'),
    path('return_book/<int:pk>/', return_book, name='return_book'),
    path('score_return/<int:pk>/', views.ScoreTheReturn.as_view(), name='score_return')
]
