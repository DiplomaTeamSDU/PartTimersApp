import random
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Freelancer, Company,CustomUser, Job
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

class FreelancerForm(forms.ModelForm):
    class Meta:
        model = Freelancer
        fields = ['bio', 'photo', 'skills', 'education', 'experience', 'portfolio_link']

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'description', 'category', 'salary', 'is_featured']