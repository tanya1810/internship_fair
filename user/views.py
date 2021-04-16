from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from .forms import UserRegistrationForm
from django.contrib.auth.forms import AuthenticationForm
from .models import User


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.email          = form.cleaned_data.get('email')
            user.save()
            

            messages.success(request, f'Your account has been created! You can login now.')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'user/login.html', {'form': form})
    


@login_required
def logout(request):
	return render(request, 'home/index.html')
