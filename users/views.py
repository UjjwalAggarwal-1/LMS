from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import StuProfileUpdateForm, LibProfileUpdateForm
from django.contrib.auth.decorators import login_required
from all_books.models import Issue


@login_required
def student_profile(request):
    if request.method == 'POST':
        p_form = StuProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if p_form.is_valid():
            p_form.save()
            messages.success(request, '!!Your account is now updated!!')
            return redirect('all_books_home')
    else:
        p_form = StuProfileUpdateForm(instance=request.user.profile)

    stu_iss_qs = Issue.objects.filter(student=request.user)
    tscore = 0
    tcount = stu_iss_qs.count()

    for data in stu_iss_qs:
        tscore += data.score
        if data.score == 0:
            tcount -= 1
    merit_score = tscore / tcount
    merit_score = round(merit_score, 3)
    context = {'title': 'Profile', 'p_form': p_form, 'mets': merit_score}
    return render(request, 'users/student_profile.html', context)


@login_required
def librarian_profile(request):
    if request.method == 'POST':
        p_form = LibProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if p_form.is_valid():
            p_form.save()
            messages.success(request, '!!Your account is now updated!!')
            return redirect('librarian_home')
    else:
        p_form = LibProfileUpdateForm(instance=request.user.profile)
    context = {'title': 'Profile', 'p_form': p_form}
    return render(request, 'users/librarian_profile.html', context)


def login_redirect_view(request):
    if request.user.profile.librarian:
        return redirect('librarian_home')
    else:
        return redirect('all_books_home')