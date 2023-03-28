from audioop import avg
import datetime
import re
from django import forms
from django.forms.widgets import DateInput
from django.core.exceptions import ValidationError
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.shortcuts import get_object_or_404, render

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_short_name(self):
        return self.first_name
    
    def get_rating(self):
        return self.ratings.aggregate(avg('rating'))['rating__avg']

class Rating(models.Model):
    RATING_CHOICES = (
        (1, '1 star'),
        (2, '2 stars'),
        (3, '3 stars'),
        (4, '4 stars'),
        (5, '5 stars'),
    )
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='ratings')
    rating = models.IntegerField(choices=RATING_CHOICES)
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Company(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    field = models.CharField(max_length=30, blank=True)
    description = models.TextField(blank=True)
    logo = models.ImageField(default='default_picture.png', upload_to='company_profile_images', blank=True)
    def get_rating(self):
        return self.user.get_rating()

class Skill(models.Model): 
    name = models.CharField(max_length=50) 
    def __str__(self):
        return self.name

class Freelancer(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE) 
    first_name = models.CharField(default='', max_length=20)
    last_name = models.CharField(default='', max_length=20)
    occupation = models.CharField(default='', max_length=20)
    level = models.CharField(default='', max_length=15)
    bio = models.TextField()
    photo = models.ImageField(default='default_picture.png', upload_to='freelancer_profile_images', blank=True)
    skills = models.ManyToManyField(Skill) 
    # education = models.TextField()
    education_university = models.CharField(default='', max_length=30)
    education_specialization = models.CharField(default='', max_length=30)
    education_year_of_study = models.CharField(default='', max_length=20)
    # experience = models.TextField()
    experience_position = models.CharField(default='', max_length=30)
    experience_company_name = models.CharField(default='', max_length=30)
    experience_work_duration = models.CharField(default='', max_length=20)
    experience_description = models.TextField(default='')
    created_at = models.DateTimeField(auto_now_add=True)
    portfolio_link = models.URLField(blank=True)
    def get_rating(self):
        return self.user.get_rating()

class Category(models.Model):
    name = models.CharField(max_length=255) 
    
    def __str__(self):
        return self.name

class DateField(forms.DateField):
    input_formats = ['%d.%m.%Y']
    widget = forms.DateInput(format='%d.%m.%Y')

    def validate(self, value):
        super().validate(value)
        if value is not None and isinstance(value, (str, bytes)) and not re.match(r"^\d{1,2}\.\d{2}\.\d{4}$", value):
            raise ValidationError("Invalid date format. Use dd.mm.yyyy.")


class Job(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    salary = models.PositiveIntegerField(null=True, blank=True)
    timeline = models.DateField()

    def get_timeline_display(self):
        return self.timeline.strftime("%d.%m.%Y")
    


class JobApplication(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    freelancer = models.ForeignKey(Freelancer, on_delete=models.CASCADE)
    cover_letter = models.TextField()
  