from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from all_books.views import add_book, issue_request_listview, cover, issue_request_detailview
from users import views as users_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('all_books/', include('all_books.urls')),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('accounts/', include('allauth.urls')),
    path('', cover, name='cover'),
    path('profile/', users_views.profile, name='user_profile'),
    path('librarian_home/', issue_request_listview, name='librarian_home'),
    path('librarian_home/<int:issue_request_id>/', issue_request_detailview, name='librarian_home_2'),
    path('add_book/', add_book, name='add_book')
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

