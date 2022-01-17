from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm
from django.contrib.auth.decorators import login_required


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'hey, {username}! Your account is now created, you may login!!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {"form": form})


def cover(request):
    return render(request, 'all_books/cover.html', {'title': 'cover_page'})


@login_required
def profile(request):
    return render(request, 'users/profile.html', {'title': 'user_profile'})