from django.http import JsonResponse 
from django.shortcuts import get_object_or_404, render, redirect 
from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Count,Q
from django.core.paginator import Paginator
from rest_framework_simplejwt.tokens import AccessToken 
from rest_framework.decorators import api_view, permission_classes 
from rest_framework.permissions import IsAuthenticated 
from django.contrib import messages, auth 
from django.urls import reverse_lazy 
from .forms import CompanyForm, FreelancerForm, JobApplicationForm, JobForm 
from jobs.forms import RegistrationForm 
from .models import Category, Company, CustomUser, Freelancer, Job, JobApplication 
 
def home(request): 
    return render(request, 'homepage.html') 

def is_company(user):
    return hasattr(user, 'company')
 
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('home')
    else:
        form = RegistrationForm()
    return render(request, 'registerpage.html', {'form': form})
 
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
            return render(request, 'loginpage.html', context=context) 
    else: 
        return render(request, 'loginpage.html') 
     
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
        job_list = Job.objects.filter(company=profile)
        paginator = Paginator(job_list, 4) # Show 4 jobs per page
        page = request.GET.get('page')
        jobs = paginator.get_page(page)
    else: 
        profile = user.freelancer 
        role = 'freelancer' 
        jobs = None
    return render(request, 'registration/profile.html', {'profile': profile, 'role': role, 'jobs': jobs}) 

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
            form.save_m2m() 
            return redirect('profile') 
    else: 
        form = form_class(instance=profile) 
    return render(request, 'registration/edit_profile.html', {'form': form})

@user_passes_test(is_company)
@login_required
def company_dashboard(request):
    company = request.user.company
    jobs = Job.objects.filter(company=company)

    return render(request, 'jobs/company_dashboard.html', {'jobs': jobs})

@user_passes_test(is_company)
@login_required
def post_job(request):
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.company = request.user.company
            job.save()
            messages.success(request, 'Job posted successfully.')
            return redirect('profile')
    else:
        form = JobForm()
    return render(request, 'jobs/post_job.html', {'form': form})

@user_passes_test(is_company)
@login_required
def edit_job(request, job_id):
    job = get_object_or_404(Job, id=job_id, company=request.user.company)
    if request.method == 'POST':
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            messages.success(request, 'Job updated successfully.')
            return redirect('profile')
    else:
        form = JobForm(instance=job)
    return render(request, 'jobs/edit_job.html', {'form': form})

@login_required
def view_jobs(request):
    jobs = Job.objects.filter(is_active=True).annotate(num_applications=Count('jobapplication'))
    companies = Company.objects.all()
    categories = Category.objects.all()
    search_query = request.GET.get('search')
    company_id = request.GET.get('company')
    category_id = request.GET.get('category')
    sort_by_salary = request.GET.get('sort_by_salary')

    if search_query:
        jobs = jobs.filter(Q(title__icontains=search_query) | Q(category__name__icontains=search_query))

    if company_id:
        jobs = jobs.filter(company__id=company_id)

    if category_id:
        jobs = jobs.filter(category__id=category_id)

    if sort_by_salary:
        if sort_by_salary == 'asc':
            jobs = jobs.order_by('salary')
        elif sort_by_salary == 'desc':
            jobs = jobs.order_by('-salary')

    return render(request, 'jobs/view_jobs.html', {'jobs': jobs, 'companies': companies, 'categories': categories})

@login_required
def apply_to_job(request, job_id):
    job = Job.objects.get(id=job_id)
    form = JobApplicationForm(request.POST or None)
    if form.is_valid():
        application = form.save(commit=False)
        application.job = job
        application.freelancer = request.user.freelancer
        application.save()
        messages.success(request, 'Your application has been submitted.')
        return redirect('view_job', job_id=job_id)
    return render(request, 'jobs/apply_to_job.html', {'job': job, 'form': form})


@login_required
def view_job(request, job_id):
    job = Job.objects.get(id=job_id)
    applications = JobApplication.objects.filter(job=job)
    if request.method == 'POST' and hasattr(request.user, 'company'):
        form = FreelancerForm(request.POST)
        if form.is_valid():
            freelancers = form.cleaned_data['freelancer']
            selected_freelancers = list(freelancers.all())
            job.freelancer.set(selected_freelancers)
            messages.success(request, 'Freelancer chosen for job.')
            return redirect('view_job', job_id=job_id)
    else:
        form = FreelancerForm()
    return render(request, 'jobs/view_job.html', {'job': job, 'applications': applications, 'form': form})

@user_passes_test(is_company)
@login_required
def select_freelancer(request, job_id, application_id):
    job = Job.objects.get(id=job_id)
    application = JobApplication.objects.get(id=application_id)
    if request.user.company != job.company:
        # Redirect to error page or show error message
        pass
    application.status = 'accepted'
    application.save()
    # Notify the freelancer that their application was accepted
    return redirect('view_job', job_id=job_id)

@user_passes_test(is_company)
@login_required
def view_freelancer(request, freelancer_id):
    freelancer = Freelancer.objects.get(id=freelancer_id)
    return render(request, 'jobs/view_freelancer.html', {'freelancer': freelancer})