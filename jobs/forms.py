import random
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Category, Freelancer, Company,CustomUser, Job, Skill, TimeField, TimeInput
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
        fields = ['name', 'description', 'logo']

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
            self.save_m2m()
        return instance


class FreelancerForm(forms.ModelForm):
    # skills = forms.ModelMultipleChoiceField(
    #     queryset=Skill.objects.all(),
    #     widget=forms.CheckboxSelectMultiple,
    #     required=False
    # )

    class Meta:
        model = Freelancer
        fields = ['first_name', 'last_name', 'occupation', 'bio', 'photo', 'education', 'experience', 'portfolio_link']

    # def clean_skills(self):
    #     skills = self.cleaned_data.get('skills')
    #     if skills:
    #         try:
    #             return [int(skill_id) for skill_id in skills.split(',')]
    #         except ValueError:
    #             return Skill.objects.filter(name__in=[skill.strip() for skill in skills.split(',')])

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     if self.instance:
    #         self.fields['skills'].initial = self.instance.skills.all()

    def save(self, commit=True):
        instance = super().save(commit=False)
        # if commit:
        #     instance.save()
        #     selected_skills = self.cleaned_data['skills']
        #     instance.skills.clear()
        #     instance.skills.add(*selected_skills)
        if commit:
            instance.save()
            self.save_m2m()
        return instance

    

class JobForm(forms.ModelForm):
    timeline = TimeField(widget=TimeInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.all()

    class Meta:
        model = Job
        fields = ['title', 'description', 'category', 'salary', 'timeline']
