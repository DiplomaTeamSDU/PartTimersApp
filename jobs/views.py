from django.http import JsonResponse
from django.urls import reverse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Count, Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib import messages, auth
from .forms import CompanyForm, EducationFormSet, ExperienceFormSet, FreelancerForm, JobForm, ProjectForm, EducationForm, ExperienceForm
from jobs.forms import RegistrationForm, RatingForm, SubmissionForm
from .models import Category, Chat, Company, CustomUser, Education, Experience, Freelancer, Job, JobApplication, Rating, Project, Skill, Submission
from django.utils import timezone
 
def home(request): 
    jobs = Job.objects.filter(created_at__lte=timezone.now()).order_by('-created_at')[:8]

    categories = Category.objects.all()
    return render(request, 'home.html', {'jobs': jobs, 'categories': categories}) 


def is_company(user):
    return hasattr(user, 'company')


def is_freelancer(user):
    return hasattr(user, 'freelancer')
 

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('profile')
    else:
        form = RegistrationForm()
    return render(request, 'sign/signup.html', {'form': form})
 

def login_view(request): 
    if request.method == 'POST': 
        email = request.POST.get('email') 
        password = request.POST.get('password') 
        user = authenticate(request, email=email, password=password) 
        if user is not None: 
            login(request, user) 
            messages.success(request, ("You were logged in"))
            return redirect('home') 
        else: 
            context = {'error_message': 'Invalid login credentials'} 
            return render(request, 'sign/signin.html', context=context) 
    else: 
        return render(request, 'sign/signin.html') 
    

def logout(request): 
    auth.logout(request) 
    messages.warning(request, ("You were logged out")) 
    return redirect('home') 
 

@login_required
def profile(request):
    user = request.user
    if hasattr(user, 'company'):
        profile = user.company
        role = 'company'

        job_list = profile.job_set.all()
        paginator = Paginator(job_list, 8)
        page = request.GET.get('page')

        try:
            jobs = paginator.page(page)
        except PageNotAnInteger:
            jobs = paginator.page(1)
        except EmptyPage:
            jobs = paginator.page(paginator.num_pages)

        company_ratings = Rating.objects.filter(recipient=profile.user)
        paginator2 = Paginator(company_ratings, 3) 
        page_number = request.GET.get('page')
        page_obj = paginator2.get_page(page_number)

        project_form = None
        education_formset = None
        experience_formset = None
    else:
        profile = user.freelancer 
        role = 'freelancer' 
        freelancer_ratings = Rating.objects.filter(recipient=profile.user) 
        project_form = None   
        skills = None
 
        paginator = Paginator(freelancer_ratings, 3) 
        page_number = request.GET.get('page') 
        page_obj = paginator.get_page(page_number) 
 
        if request.method == 'POST':
            project_form = ProjectForm(request.POST, request.FILES)
            if project_form.is_valid():
                project = project_form.save(commit=False)
                project.freelancer = request.user.freelancer
                project.save()
                messages.success(request, 'Project posted successfully.')
                return redirect('profile')
            else:
                project_form = ProjectForm(instance=profile)

            educationFormSet = EducationFormSet(request.POST, instance=profile)  
            if educationFormSet.is_valid():  
                educationFormSet.save()  
                messages.success(request, 'Education added')  
                return redirect('profile')  
            else:  
                educationFormSet = EducationFormSet(instance=profile)  
  
            experienceFormSet = ExperienceFormSet(request.POST, instance=profile)  
            if experienceFormSet.is_valid():  
                experienceFormSet.save()  
                messages.success(request, 'Education added')  
                return redirect('profile')  
            else:  
                experienceFormSet = ExperienceFormSet(instance=profile)


            selected_skill_names = request.POST.getlist('skill_names')
            selected_skills = Skill.objects.filter(name__in=selected_skill_names)
            profile.skills.set(selected_skills)

            new_skills = []
            for i in range(0, 11):  # Maximum of 10 new skills
                new_skill_name = request.POST.get(f'new_skill_{i}')
                if new_skill_name:
                    new_skill_name = new_skill_name.strip()
                    if len(new_skill_name) <= 50:
                        try:
                            skill = Skill.objects.create(name=new_skill_name)
                            new_skills.append(skill)
                        except:
                            messages.warning(request, f'Could not create new skill "{new_skill_name}"')
            if new_skills:
                profile.skills.add(*new_skills)
                messages.success(request, 'Skills updated')

            

        job_list = profile.project_set.all()  
        paginator2 = Paginator(job_list, 4)  
        page = request.GET.get('page')  
 
        try:  
            jobs = paginator2.page(page)  
        except PageNotAnInteger:  
            jobs = paginator2.page(1)  
        except EmptyPage:  
            jobs = paginator2.page(paginator2.num_pages)  
 
        education_formset = EducationFormSet(instance=profile) 
        experience_formset = ExperienceFormSet(instance=profile)
 
    project_form = ProjectForm(instance=profile)
    skills = Skill.objects.all()

    

    return render(request, 'profiles/profile.html', {
        'profile': profile, 
        'role': role, 
        'jobs': jobs, 
        'page_obj': page_obj, 
        'project_form': project_form, 
        'skills': skills, 
        'education_formset': education_formset,
        'experience_formset': experience_formset})


@login_required
def edit_profile(request, role):
    user = request.user
    if role == 'company':
        profile = user.company
        form_class = CompanyForm
        job_list = profile.job_set.all()
        paginator = Paginator(job_list, 8)
        page = request.GET.get('page')
        try:
            jobs = paginator.page(page)
        except PageNotAnInteger:
            jobs = paginator.page(1)
        except EmptyPage:
            jobs = paginator.page(paginator.num_pages)
        form = form_class(instance=profile)
        if request.method == 'POST':
            form = form_class(request.POST, request.FILES, instance=profile)
            if form.is_valid():
                if form.has_changed():
                    form.save()
                    messages.success(request, 'Profile updated')
                else:
                    messages.warning(request, 'No changes made to profile')
            return redirect('profile')
            
        return render(request, 'profiles/edit_profile.html', {'form': form, 'role': role, 'profile': profile, 'jobs': jobs})
    else: 
        profile = user.freelancer 
        form_class = FreelancerForm 
        form = form_class(instance=profile) 

        project_list = profile.project_set.all()  
        paginator2 = Paginator(project_list, 4)  
        page = request.GET.get('page')  
 
        try:  
            projects = paginator2.page(page)  
        except PageNotAnInteger:  
            projects = paginator2.page(1)  
        except EmptyPage:  
            projects = paginator2.page(paginator2.num_pages) 
         
        if request.method == 'POST': 
            form = form_class(request.POST, request.FILES, instance=profile) 
     
            if form.is_valid(): 
                if form.has_changed(): 
                    form.save() 
                    messages.success(request, 'Profile updated') 
                else: 
                    messages.warning(request, 'No changes made to profile') 
            return redirect('profile') 
        
        return render(request, 'profiles/edit_profile.html', {'form': form, 'role': role, 'profile': profile, 'projects': projects})


def edit_skills(request):
    freelancer = request.user.freelancer

    if request.method == 'POST':
        # Clear current skills and add selected skills
        selected_skill_names = request.POST.getlist('skill_names')
        selected_skills = Skill.objects.filter(name__in=selected_skill_names)
        freelancer.skills.set(selected_skills)

        # Add new skills
        new_skills = []
        for i in range(1, 11):  # Maximum of 10 new skills
            new_skill_name = request.POST.get(f'new_skill_{i}')
            if new_skill_name:
                new_skill_name = new_skill_name.strip()
                if len(new_skill_name) <= 50:
                    try:
                        skill = Skill.objects.create(name=new_skill_name)
                        new_skills.append(skill)
                    except:
                        messages.warning(request, f'Could not create new skill "{new_skill_name}"')
        if new_skills:
            freelancer.skills.add(*new_skills)

        messages.success(request, 'Skills updated')
        return redirect('profile')

    # Render add_skills.html with current skills
    skills = Skill.objects.all()
    return render(request, 'profiles/edit_skills.html', {'skills': skills})


@user_passes_test(is_company)
@login_required
def company_dashboard(request):
    company = request.user.company
    jobs = Job.objects.filter(company=company)

    return render(request, 'jobs/company_dashboard.html', {'jobs': jobs})


@user_passes_test(is_company)
@login_required
def post_job(request):
    profile = Company.objects.get(user=request.user)
    if not profile.description:
        messages.error(request, 'Please add a bio before posting a job. To add a bio press Edit button.')
        return redirect(request.META.get('HTTP_REFERER'))

    if request.method == 'POST':
        form = JobForm(request.POST, request.FILES)
        if form.is_valid():
            job = form.save(commit=False)
            job.company = request.user.company
            selected_skills = form.cleaned_data['skills'] 
            job.save() 
            job.skills.set(selected_skills)
            messages.success(request, 'Job posted successfully')
            return redirect('profile')
    else:
        form = JobForm()
    return render(request, 'jobs/post_job.html', {'form': form})


@user_passes_test(is_freelancer)
@login_required
def post_project(request):
    freelancer = Freelancer.objects.get(user=request.user)

    if not freelancer.bio:
        messages.error(request, 'Please add a bio before posting a project. To add a bio press Edit button.')
        return redirect(request.META.get('HTTP_REFERER'))

    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.freelancer = freelancer
            project.save()
            messages.success(request, 'Project has been posted successfully.')
            return redirect('dashboard')
    else:
        form = ProjectForm()
    return render(request, 'modals/post_project.html', {'form': form})


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


# @login_required
def view_jobs(request): 
    job_list = Job.objects.filter(is_active=True, status='pending').annotate(num_applications=Count('jobapplication')) 
    jobs_popular = Job.objects.filter(is_active=True, status='pending').annotate(num_applications=Count('jobapplication')).order_by('-num_applications')[:4] 
    categories = Category.objects.all() 
    search_query = request.GET.get('search') 
    category_id = request.GET.get('category') 
    salary_range = request.GET.get('salary_range') 
 
    # Filter jobs by search query, company, category, and sort order 
    if search_query: 
        job_list = job_list.filter(Q(title__icontains=search_query) | Q(category__name__icontains=search_query)) 
 
    if category_id: 
        job_list = job_list.filter(category__id=category_id) 
 
    if salary_range: 
        if salary_range == '0-500': 
            job_list = job_list.filter(salary__range=(0, 500)) 
        elif salary_range == '500-1000': 
            job_list = job_list.filter(salary__range=(500, 1000)) 
        elif salary_range == '1000-5000': 
            job_list = job_list.filter(salary__range=(1000, 5000)) 
        elif salary_range == '5000-10000': 
            job_list = job_list.filter(salary__range=(5000, 10000)) 
        elif salary_range == '10000+': 
            job_list = job_list.filter(salary__gte=10000) 
 
    paginator = Paginator(job_list, 16)   
    page = request.GET.get('page') 
    try: 
        jobs = paginator.page(page) 
    except PageNotAnInteger: 
        jobs = paginator.page(1) 
    except EmptyPage: 
        jobs = paginator.page(paginator.num_pages) 
 
    return render(request, 'jobs/view_jobs.html', {'jobs': jobs, 'categories': categories, 'jobs_popular': jobs_popular})


@user_passes_test(is_freelancer)
@login_required
def apply_to_job(request, job_id):
    job = Job.objects.get(id=job_id)

    freelancer = Freelancer.objects.get(user=request.user)

    if not freelancer.bio:
        messages.error(request, 'Please add a bio before applying a job')
        return redirect(request.META.get('HTTP_REFERER'))

    if hasattr(request.user, 'freelancer'):
        application_exists = JobApplication.objects.filter(job=job, freelancer=request.user.freelancer).exists()

        if application_exists:
            messages.error(request, 'You have already applied to this job')
        else:
            application = JobApplication.objects.create(job=job, freelancer=request.user.freelancer)
            messages.success(request, 'Your application has been submitted')
    else:
        messages.error(request, 'You must be a freelancer to apply to this job')

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
    if job.status == 'completed':    # Check if the user has already rated the job
        existing_rating = Rating.objects.filter(job=job, reviewer=request.user).exists()
        if existing_rating:        # User has already rated the job, do not show the rating button
            show_rating_button = False    
        else:
            # User has not rated the job yet, show the rating button        
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
    freelancer_ratings = Rating.objects.filter(recipient=freelancer.user) 
    paginator = Paginator(freelancer_ratings, 3) 
    page_number = request.GET.get('page') 
    reviews = paginator.get_page(page_number)
    educations = Education.objects.filter(freelancer=freelancer)  # Query the education records for the freelancer 
    experiences = Experience.objects.filter(freelancer=freelancer)  # Query the experience records for the freelancer 
    projects = Project.objects.filter(freelancer=freelancer)

    # project_list = profile.project_set.all()   
    paginator2 = Paginator(projects, 4)   
    page = request.GET.get('page')   
  
    try:   
        projects = paginator2.page(page)   
    except PageNotAnInteger:   
        projects = paginator2.page(1)   
    except EmptyPage:   
        projects = paginator2.page(paginator2.num_pages)
     
    return render(request, 'jobs/view_freelancer.html', {'freelancer': freelancer, 'reviews': reviews, 'educations': educations, 'experiences': experiences, 'projects': projects})



@user_passes_test(is_company)
@login_required
def find_freelancer(request):
    # freelancer = Freelancer.objects.get(user=request.user)

    # if freelancer:
    #     messages.warning(request, 'You cannot view this page unless you are an employer')
    #     return redirect(request.META.get('HTTP_REFERER'))

    freelancers_list = Freelancer.objects.all()
    search_query = request.GET.get('search')

    if search_query:
        freelancers_list = freelancers_list.filter(Q(first_name__icontains=search_query) | Q(last_name__icontains=search_query) |
                                                    Q(occupation__icontains=search_query) | Q(bio__icontains=search_query))

    paginator = Paginator(freelancers_list, 12)  
    page = request.GET.get('page')
    try:
        freelancers_list = paginator.page(page)
    except PageNotAnInteger:
        freelancers_list = paginator.page(1)
    except EmptyPage:
        freelancers_list = paginator.page(paginator.num_pages)

    return render(request, 'jobs/find_freelancer_page.html', {'freelancers': freelancers_list})


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


# @user_passes_test(is_company)
# @login_required
# def view_freelancer(request, freelancer_id):
#     freelancer = Freelancer.objects.get(id=freelancer_id)
#     return render(request, 'jobs/view_freelancer.html', {'freelancer': freelancer})

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


@login_required 
def active_projects(request): 
    if hasattr(request.user, 'company'):  
        company = request.user.company    
        jobs = Job.objects.filter(company=company, jobapplication__isnull=False).distinct() 
        applications = {}    
        submissions={} 
        for job in jobs:  
            applications[job.id] = job.jobapplication_set.all()  
            submissions[job.id]=job.submission_set.all()  
        if request.method == 'POST': 
            submission_id = request.POST.get('submission_id') 
            submission = get_object_or_404(Submission, id=submission_id, job__company=company) 
            if submission.status != 'pending': 
                messages.error(request, "The job submission is not in pending review status.") 
            else: 
                if request.POST.get('action') == 'accept': 
                    submission.status = 'accepted'  
                    submission.save()
                    submission.job.status = 'completed'  
                    submission.job.save()  
                    messages.success(request, "Job submitted successfully.") 
                else: 
                    messages.error(request, "Invalid action.") 

        return render(request, 'jobs/active_projects.html', {'jobs': jobs, 'applications': applications,'submissions': submissions})
         
    elif hasattr(request.user, 'freelancer'):  
        if request.method == 'POST': 
            job_id = request.POST.get('job_id') 
            job = get_object_or_404(Job, id=job_id) 
            form = SubmissionForm(request.POST, request.FILES)  
            if form.is_valid():   
                existing_submission = Submission.objects.filter(job=job, freelancer=request.user.freelancer).first() 
                if existing_submission: 
                    # If an existing submission exists, update it 
                    existing_submission.link = form.cleaned_data['link'] 
                    existing_submission.file = form.cleaned_data['file'] 
                    existing_submission.save() 
                    messages.success(request, "You resubmitted project successfully")
                else: 
                    # Create a new submission 
                    submission = form.save(commit=False) 
                    submission.job = job 
                    submission.freelancer = request.user.freelancer 
                    submission.save() 
                    messages.success(request, "You submitted project successfully")
                job.status = 'pending_review'   
                job.save()   
                return redirect('active_projects')  
        else:  
            form = SubmissionForm()  
        applications = JobApplication.objects.filter(freelancer=request.user.freelancer)  
        return render(request, 'jobs/active_projects.html', {'applications': applications,'form': form,}) 
 
    return render(request, 'jobs/active_projects.html', {'applications': applications})




# @login_required
# def active_projects(request):
#     if hasattr(request.user, 'company'): 
#         company = request.user.company   
#         jobs = Job.objects.filter(company=company, jobapplication__isnull=False).distinct()
#         applications = {}   
#         for job in jobs: 
#             applications[job.id] = job.jobapplication_set.all() 
#         return render(request, 'jobs/active_projects.html', {'jobs': jobs, 'applications': applications}) 
 
#     elif hasattr(request.user, 'freelancer'): 
#         applications = JobApplication.objects.filter(freelancer=request.user.freelancer) 

#     return render(request, 'jobs/active_projects.html', {'applications': applications})


# @login_required
# def submit_work(request, job_id): 
#     job = get_object_or_404(Job, id=job_id) 
#     if request.method == 'POST': 
#         form = SubmissionForm(request.POST, request.FILES) 
#         if form.is_valid(): 
#             submission = form.save(commit=False) 
#             submission.id=job.id 
#             submission.job = job 
#             submission.freelancer = request.user.freelancer 
#             submission.save() 
#             job.status = 'pending_review' 
#             job.save() 
#             return redirect('view_job', job_id=job.id) 
#     else: 
#         form = SubmissionForm() 
#     return render(request, 'jobs/submit_work.html', {'form': form, 'job': job}) 
 
def view_submission(request, submission_id): 
    submission = get_object_or_404(Submission, id=submission_id) 
    job = submission.job 
    if request.method == 'POST': 
        if 'accept_work' in request.POST: 
            job.status = 'progress' 
            job.save() 
    return render(request, 'jobs/view_submission.html', {'submission': submission, 'job': job}) 
 
@login_required 
def accept_submission(request, submission_id): 
    submission = get_object_or_404(Submission, id=submission_id) 
 
    # Ensure that only the company who posted the job can accept submissions 
    if request.user != submission.job.company.user: 
        messages.error(request, 'you cant') 
 
    # Update the submission status to "accepted" 
    submission.status = 'accepted' 
    submission.save() 
 
    # Update the job status to "completed" 
    submission.job.status = 'completed' 
    submission.job.save() 
 
    # Redirect to the view_submission page 
    return redirect('view_submission', submission_id=submission.id)
     