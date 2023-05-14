import random
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Category, DateField, Freelancer, Company, CustomUser, Job, JobApplication, Rating, Education, Experience, Project, Skill, Submission
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.forms import inlineformset_factory


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text='Enter a valid email address')

    CHOICES = (
        ('freelancer', 'I am a freelancer'),
        ('company', 'I am an employer (company)'),
    )

    choice = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)

    class Meta:
        model = CustomUser
        fields = ['first_name','last_name','email', 'password1', 'password2', 'choice']

    def clean_email(self):
        email = self.cleaned_data['email']
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("This email address is already in use. Please use a different email.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        choice = self.cleaned_data['choice']
        if choice == 'freelancer':
            Freelancer.objects.create(user=user)
        else:
            Company.objects.create(user=user)
        return user


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name', 'field', 'description', 'logo', 'skills', 'instagram_link', 'linkedin_link', 'facebook_link', 'website_link']

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
            self.save_m2m()
        return instance


class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        fields = ['university', 'specialization', 'year_of_study']


class ExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        fields = ['position', 'company_name', 'work_duration', 'description']


class SkillForm(forms.Form):
    name = forms.CharField(max_length=50, label="Add Skill", required=False)

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get("name")

        if not name:
            raise forms.ValidationError("You must add a skill.")

        return cleaned_data

EducationFormSet = inlineformset_factory(Freelancer, Education, form=EducationForm, extra=1, can_delete=True)
ExperienceFormSet = inlineformset_factory(Freelancer, Experience, form=ExperienceForm, extra=1, can_delete=True)

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'link', 'platform']


class FreelancerForm(forms.ModelForm):
    class Meta:
        model = Freelancer
        fields = ['first_name', 'last_name', 'occupation', 'level', 'bio', 
                  'photo', 'portfolio_link']
        
    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
            self.save_m2m()
        return instance
    

class JobForm(forms.ModelForm): 
    skills = forms.ModelMultipleChoiceField( 
        queryset=Skill.objects.all(), 
        widget=forms.SelectMultiple(attrs={'size': 5}), 
        required=False, 
        label='Skills' 
    ) 
    def __init__(self, *args, **kwargs): 
        super().__init__(*args, **kwargs) 
        self.fields['category'].queryset = Category.objects.all() 
    def __init__(self, *args, **kwargs): 
        super().__init__(*args, **kwargs) 
        if self.instance.pk: 
            selected_skills = self.instance.skills.values_list('id', flat=True) 
            self.initial['skills'] = selected_skills 
    class Meta: 
        model = Job 
        fields = ['title', 'description', 'file', 'category', 'position', 'salary', 'timeline'] 
        widgets = { 
            'timeline': forms.DateInput(format='%d.%m.%Y') 
        } 
        field_classes = { 
            'timeline': DateField 
        }

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['rating', 'comment']
        labels = {
            'rating': 'Rating (out of 5 stars)',
            'comment': 'Comment (optional)',
        }
        widgets = {
            'rating': forms.RadioSelect(choices=Rating.RATING_CHOICES),
            'comment': forms.Textarea(attrs={'rows': 3}),
        }


class JobApplicationForm(forms.ModelForm):
     
    cover_letter = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = JobApplication
        fields = ['cover_letter']


class SubmissionForm(forms.ModelForm): 
    link = forms.URLField(max_length=255, required=False) 
    file = forms.FileField(required=False)

    class Meta: 
        model = Submission 
        fields = ['link', 'file']