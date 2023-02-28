from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Freelancer, Company

class RegistrationForm(UserCreationForm):
    CHOICES = (
        ('freelancer', 'I am a freelancer'),
        ('company', 'I am a company'),
    )

    choice = forms.ChoiceField(choices=CHOICES)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'choice']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['username']
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