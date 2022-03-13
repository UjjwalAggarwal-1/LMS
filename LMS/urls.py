from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from all_books.views import add_book, issue_request_listview, cover, request_decision, reject_request
from users import views as users_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('all_books/', include('all_books.urls')),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('', cover, name='cover'),
    path('accounts/', include('allauth.urls')),
    path('student_profile/', users_views.student_profile, name='student_profile'),
    path('librarian_profile/', users_views.librarian_profile, name='librarian_profile'),
    path('librarian_controls/', issue_request_listview, name='librarian_controls'),
    path('librarian_controls/<int:issue_request_id>/', request_decision, name='request_decision'),
    path('librarian_controls/<int:issue_request_id>/reject/', reject_request, name='reject_request'),
    path('add_book/', add_book, name='add_book'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

