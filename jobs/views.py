from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages, auth
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from .forms import CompanyForm, FreelancerForm
from jobs.forms import RegistrationForm
from .models import Company, Job


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(request, username=username, password=password)
            login(request, user)
            return redirect('profile')
    else:
        form = RegistrationForm()
    return render(request, 'registration/register.html', {'form': form})


class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    success_url = reverse_lazy('profile')

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
            return render(request, 'registration/login.html', context=context)
    else:
        return render(request, 'registration/login.html')
    
def logout(request):
    auth.logout(request)
    messages.success(request, ("You were logged out"))
    return redirect('home')

@login_required
def profile(request):
    user = request.user
    if hasattr(user, 'company'):
        profile = user.company
        role = 'company'
    else:
        profile = user.freelancer
        role = 'freelancer'
    return render(request, 'registration/profile.html', {'profile': profile, 'role': role})

@login_required
def edit_profile(request, role):
    user = request.user
    if role == 'company':
        profile = user.company
        form_class = CompanyForm
    else:
        profile = user.freelancer
        form_class = FreelancerForm
    if request.method == 'POST':
        form = form_class(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = form_class(instance=profile)
    return render(request, 'registration/edit_profile.html', {'form': form})

def index(request):
    return render(request, 'homepage.html')