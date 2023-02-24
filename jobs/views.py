from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages, auth
from .models import Company, Job

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(request, username=username, password=password)
            login(request, user)
            return redirect('profile')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            context = {'error_message': 'Invalid login credentials'}
            return render(request, 'login.html', context=context)
    else:
        return render(request, 'registration/login.html')
    
def logout(request):
    auth.logout(request)
    messages.success(request, ("You were logged out"))
    return redirect('home')

def profile(request):
    user = request.user
    try:
        company = user.company
    except Company.DoesNotExist:
        company = None
    return render(request, 'registration/profile.html', {'user': user, 'company': company})

def index(request):
    return render(request, 'base.html')