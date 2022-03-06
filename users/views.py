from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ProfileUpdateForm
from django.contrib.auth.decorators import login_required


@login_required
def profile(request):
    if request.method == 'POST':
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if p_form.is_valid():
            p_form.save()
            messages.success(request, '!!Your account is now updated!!')
            return redirect('all_books_home')
    else:
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {'title': 'Profile', 'p_form': p_form}

    return render(request, 'users/profile.html', context)


def login_redirect_view(request):
    if request.user.profile.librarian:
        return redirect('librarian_home')
    else:
        return redirect('all_books_home')