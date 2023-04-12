from django.http import JsonResponse
from django.urls import reverse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Count, Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib import messages, auth
from .forms import CompanyForm, FreelancerForm, JobForm
from jobs.forms import RegistrationForm, RatingForm
from .models import Category, Chat, Company, CustomUser, Freelancer, Job, JobApplication
from django.utils import timezone
 
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
            return redirect('profile')
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
        job_list = profile.job_set.all()
        paginator = Paginator(job_list, 6)
        page = request.GET.get('page')
        try:
            jobs = paginator.page(page)
        except PageNotAnInteger:
            jobs = paginator.page(1)
        except EmptyPage:
            jobs = paginator.page(paginator.num_pages)
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
        job_list = profile.job_set.all()
        paginator = Paginator(job_list, 6)
        page = request.GET.get('page')
        try:
            jobs = paginator.page(page)
        except PageNotAnInteger:
            jobs = paginator.page(1)
        except EmptyPage:
            jobs = paginator.page(paginator.num_pages)
    else:
        profile = user.freelancer
        form_class = FreelancerForm
        jobs = None
    if request.method == 'POST':
        form = form_class(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            form.save_m2m()
            return redirect('profile')
    else:
        form = form_class(instance=profile)
    return render(request, 'registration/edit_profile.html', {'form': form, 'role': role, 'profile': profile, 'jobs': jobs})


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
        form = JobForm(request.POST, request.FILES)
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
    job_list = Job.objects.filter(is_active=True).annotate(num_applications=Count('jobapplication'))
    companies = Company.objects.all()
    categories = Category.objects.all()
    search_query = request.GET.get('search')
    company_id = request.GET.get('company')
    category_id = request.GET.get('category')
    sort_by_salary = request.GET.get('sort_by_salary')

    # Filter jobs by search query, company, category, and sort order
    if search_query:
        job_list = job_list.filter(Q(title__icontains=search_query) | Q(category__name__icontains=search_query))

    if company_id:
        job_list = job_list.filter(company__id=company_id)

    if category_id:
        job_list = job_list.filter(category__id=category_id)

    if sort_by_salary:
        if sort_by_salary == 'asc':
            job_list = job_list.order_by('salary')
        elif sort_by_salary == 'desc':
            job_list = job_list.order_by('-salary')

    paginator = Paginator(job_list, 16)  
    page = request.GET.get('page')
    try:
        jobs = paginator.page(page)
    except PageNotAnInteger:
        jobs = paginator.page(1)
    except EmptyPage:
        jobs = paginator.page(paginator.num_pages)

    return render(request, 'jobs/view_jobs.html', {'jobs': jobs, 'companies': companies, 'categories': categories})


@login_required
def apply_to_job(request, job_id):
    job = Job.objects.get(id=job_id)

    if hasattr(request.user, 'freelancer'):
        application_exists = JobApplication.objects.filter(job=job, freelancer=request.user.freelancer).exists()

        if application_exists:
            messages.error(request, 'You have already applied to this job.')
        else:
            application = JobApplication.objects.create(
                job=job, freelancer=request.user.freelancer)
            messages.success(request, 'Your application has been submitted.')
    else:
        messages.error(request, 'You must be a freelancer to apply to this job.')

    return redirect('applications')


@login_required
def view_job(request, job_id):
    job = Job.objects.get(id=job_id)
    
    # Check if the job has a chosen freelancer
    if job.freelancer:
        # If the current user is the company and the job has a chosen freelancer, don't show the applications
        if hasattr(request.user, 'company') and request.user.company == job.company:
            applications = None
            num_applications = 0
        else:
            applications = JobApplication.objects.filter(job=job)
            num_applications = applications.count()
    else:
        applications = JobApplication.objects.filter(job=job)
        num_applications = applications.count()
    
    # Check if the current user is the chosen freelancer and the job status is 'in progress' to show the submit button
    if hasattr(request.user, 'freelancer') and request.user.freelancer == job.freelancer and job.status == 'progress':
        show_submit_button = True
    else:
        show_submit_button = False
    
    # Check if the current user is the company and the job status is 'completed' to show the rating button
    if job.status == 'completed':
        show_rating_button = True
    else:
        show_rating_button = False
    
    if request.method == 'POST' and hasattr(request.user, 'company'):
        form = FreelancerForm(request.POST)
        if form.is_valid():
            freelancer = form.save(commit=False)
            # Check if the freelancer has already applied to the job
            if JobApplication.objects.filter(job=job, freelancer=request.user.freelancer).exists():
                messages.error(request, 'You have already applied to this job.')
            else:
                selected_freelancers = list(form.cleaned_data['freelancer'].all())
                if request.user.company == job.company:
                    job.freelancer.set(selected_freelancers)
                    messages.success(request, 'Freelancer chosen for job.')
                    JobApplication.objects.filter(job=job).delete()
                    return redirect('view_job', job_id=job_id)
                else:
                    messages.error(request, 'You do not have permission to choose a freelancer for this job.')
    else:
        form = FreelancerForm()
        # Check if the freelancer has already applied to the job
        if hasattr(request.user, 'freelancer') and JobApplication.objects.filter(job=job, freelancer=request.user.freelancer).exists():
            form = None
    
    return render(request, 'jobs/view_job.html', {
        'job': job, 
        'applications': applications, 
        'form': form, 
        'num_applications': num_applications,
        'show_submit_button': show_submit_button,
        'show_rating_button': show_rating_button,
    })

@login_required
def see_applications(request):
    if hasattr(request.user, 'company'): 
        company = request.user.company   
        jobs = Job.objects.filter(company=company, jobapplication__isnull=False).distinct()
        applications = {}   
        for job in jobs: 
            applications[job.id] = job.jobapplication_set.all() 
        return render(request, 'jobs/applications.html', {'jobs': jobs, 'applications': applications}) 
 
    elif hasattr(request.user, 'freelancer'): 
        applications = JobApplication.objects.filter(freelancer=request.user.freelancer) 

    return render(request, 'jobs/applications.html', {'applications': applications})


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
    selected_freelancers = [application.freelancer]
    if job.freelancer:
        job.freelancer.set(selected_freelancers)
    else:
        job.freelancer = selected_freelancers[0]
    job.status = 'progress'
    job.save()
    # Notify the freelancer that their application was accepted
    return redirect('view_job', job_id=job_id)


@user_passes_test(is_company)
@login_required
def view_freelancer(request, freelancer_id):
    freelancer = Freelancer.objects.get(id=freelancer_id)
    return render(request, 'jobs/view_freelancer.html', {'freelancer': freelancer})

@user_passes_test(is_company)
@login_required
def find_freelancer(request):
    freelancers_list = Freelancer.objects.all()
    search_query = request.GET.get('search')

    if search_query:
        freelancers_list = freelancers_list.filter(Q(first_name__icontains=search_query) | Q(last_name__icontains=search_query) |
                                                    Q(occupation__icontains=search_query) | Q(bio__icontains=search_query))

    return render(request, 'jobs/find_freelancer_page.html', {'freelancers': freelancers_list})


@login_required
def submit_work(request, job_id):
    job = Job.objects.get(id=job_id)
    if request.user.freelancer == job.freelancer and job.status == 'progress':
        job.status = 'completed'
        job.save()
        messages.success(request, 'Work submitted successfully.')
    else:
        messages.error(request, 'Cannot submit work for this job.')
    return redirect('view_job', job_id=job_id)

def rate(request, job_id, recipient_id): 
    job = get_object_or_404(Job, pk=job_id) 
    recipient = get_object_or_404(CustomUser, pk=recipient_id) 
 
    if request.method == 'POST': 
        form = RatingForm(request.POST) 
        if form.is_valid(): 
            rating = form.save(commit=False) 
            rating.job = job 
            rating.reviewer = request.user 
            rating.recipient = recipient 
            rating.save() 
            messages.success(request, 'Thank you for rating!') 
            return redirect('view_job', job_id=job_id) 
    else: 
        form = RatingForm() 
        
    return render(request, 'jobs/rate.html', {'job': job, 'recipient': recipient, 'form': form})


@user_passes_test(is_company)
@login_required
def view_freelancer(request, freelancer_id):
    freelancer = Freelancer.objects.get(id=freelancer_id)
    return render(request, 'jobs/view_freelancer.html', {'freelancer': freelancer})

@login_required
def chats(request):
    return render(request, 'jobs/chats.html')


@login_required
def chat(request, receiver_id):
    if hasattr(request.user, 'freelancer'):
        sender = request.user.freelancer
        receiver = Company.objects.get(id=receiver_id)
    elif hasattr(request.user, 'company'):
        sender = request.user.company
        receiver = Freelancer.objects.get(id=receiver_id)

    if request.method == 'POST':
        message = request.POST.get('message')
        Chat.objects.create(sender=sender.user, receiver=receiver.user,
                            message=message, timestamp=timezone.now())

    chat_messages = Chat.objects.filter(Q(sender=sender.user, receiver=receiver.user) | Q(
        sender=receiver.user, receiver=sender.user)).order_by('timestamp')

    context = {
        'sender': sender,
        'receiver': receiver,
        'chat_messages': chat_messages,
    }

    return render(request, 'jobs/chats.html', context)