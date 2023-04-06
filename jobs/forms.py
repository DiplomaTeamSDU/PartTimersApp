import random
from django import forms
from django.forms.widgets import DateInput
from django.contrib.auth.forms import UserCreationForm
from .models import Category, DateField, Freelancer, Company, CustomUser, Job, Skill, JobApplication, Rating
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text='Enter a valid email address')

    CHOICES = (
        ('freelancer', 'I am a freelancer'),
        ('company', 'I am a company'),
    )

    choice = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)

    class Meta:
        model = CustomUser
        fields = ['email', 'password1', 'password2', 'choice']

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
        fields = ['name', 'field', 'description', 'logo']

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
            self.save_m2m()
        return instance


class FreelancerForm(forms.ModelForm):
    skills = forms.ModelMultipleChoiceField( 
        queryset=Skill.objects.all(), 
        widget=forms.SelectMultiple 
    ) 

    class Meta:
        model = Freelancer
        fields = ['first_name', 'last_name', 'occupation', 'level', 'bio', 
                  'photo', 'education_university', 
                  'education_specialization', 'education_year_of_study', 
                  'experience_position', 'experience_company_name',
                  'experience_work_duration', 'experience_description',
                  'portfolio_link','skills']

    def init(self, args, **kwargs):
        super().init(args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['skills'].initial = self.instance.skills.all()
        
    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
            self.save_m2m()
        return instance

    

class JobForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.all()

    class Meta:
        model = Job
        fields = ['title', 'description', 'file', 'category', 'salary', 'timeline']
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