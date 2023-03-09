from django.http import JsonResponse 
from django.shortcuts import render, redirect 
from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.decorators import login_required 
from rest_framework_simplejwt.tokens import AccessToken 
from rest_framework.decorators import api_view, permission_classes 
from rest_framework.permissions import IsAuthenticated 
from django.contrib import messages, auth 
from django.urls import reverse_lazy 
from .forms import CompanyForm, FreelancerForm, JobForm 
from jobs.forms import RegistrationForm 
from .models import Company, CustomUser, Job 
 
def home(request): 
    return render(request, 'homepage.html') 
 
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('home')
    else:
        form = RegistrationForm()
    return render(request, 'registration/register.html', {'form': form})
 
def login_view(request): 
    if request.method == 'POST': 
        email = request.POST.get('email') 
        password = request.POST.get('password') 
        user = authenticate(request, email=email, password=password) 
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

@login_required
def company_dashboard(request):
    company = request.user.company
    jobs = Job.objects.filter(company=company)

    return render(request, 'jobs/company_dashboard.html', {'jobs': jobs})

@login_required
def post_job(request):
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.company = request.user.company
            job.save()
            messages.success(request, 'Job posted successfully.')
            return redirect('company_dashboard')
    else:
        form = JobForm()
    return render(request, 'jobs/post_job.html', {'form': form})
