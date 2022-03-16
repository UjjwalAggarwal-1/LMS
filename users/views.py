from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import StuProfileUpdateForm, LibProfileUpdateForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
import math


@login_required
def student_profile(request):
    if request.method == 'POST':
        p_form = StuProfileUpdateForm(request.POST, instance=request.user.profile)
        if p_form.is_valid():
            if p_form.full_clean():
                p_form.save()
                messages.success(request, '!!Your account is now updated!!')
                return redirect('all_books_home')
    else:
        p_form = StuProfileUpdateForm(instance=request.user.profile)

    context = {'title': 'PROFILE', 'p_form': p_form}
    return render(request, 'users/student_profile.html', context)


@login_required
def librarian_profile(request):
    if request.method == 'POST':
        p_form = LibProfileUpdateForm(request.POST, instance=request.user.profile)  # if image field in form then add request.FILES
        if p_form.is_valid():
            mobile_num = p_form.cleaned_data.get('mobile_num')
            if math.floor(math.log10(mobile_num)+1) == 10:
                p_form.save()
                messages.success(request, '!!Your account is now updated!!')
                return redirect('librarian_controls')
            else:
                messages.warning(request, 'please fill out your 10 digit mobile number')
                return HttpResponseRedirect(request.path)
    else:
        p_form = LibProfileUpdateForm(instance=request.user.profile)

    context = {'title': 'PROFILE', 'p_form': p_form}
    return render(request, 'users/librarian_profile.html', context)


def login_redirect_view(request):
    if request.user.profile.librarian:
        return redirect('librarian_controls')
    else:
        return redirect('all_books_home')
