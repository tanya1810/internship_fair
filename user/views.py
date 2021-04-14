from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from .forms import StudentRegisterForm, StudentUpdateForm
from django.contrib.auth.forms import AuthenticationForm
from .models import User, StudentProfile


def studentregister(request):
    if request.method == 'POST':
        form = StudentRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.email          = form.cleaned_data.get('email')
            user.save()
            student             = StudentProfile.objects.create(user=user)
            student.college     = form.cleaned_data.get('college')
            student.contact     = form.cleaned_data.get('contact')
            student.name        = form.cleaned_data.get('name')
            student.cgpa        = form.cleaned_data.get('cgpa')
            student.area_of_specialization  = form.cleaned_data.get('area_of_specialization')
            student.year_of_study           = form.cleaned_data.get('year_of_study')
            student.city_of_residence       = form.cleaned_data.get('city_of_residence')
            student.save()

            messages.success(request, f'Your account has been created! You can login now.')
            return redirect('login')
    else:
        form = StudentRegisterForm()
    return render(request, 'user/signup-student.html', {'form': form})
    

@login_required
def profileupdate(request):
        if request.method == 'POST':
            form = StudentUpdateForm(request.POST, request.FILES, instance=request.user.student_profile)

            if form.is_valid():
                form.save()
                messages.success(request, f'Account update successfully!')
                return redirect('profile')

        else:
            form = StudentUpdateForm(instance=request.user.student_profile)
        context = {
            'form': form,
        }

        return render(request, 'user/profile-update.html', context)

@login_required   
def profile(request):
        context = {
            'object': request.user.student_profile,
        }

        return render(request, 'user/student_profile.html', context)
    


@login_required
def logout(request):
	return render(request, 'startupEcosystem/ecosystem-home.html')
