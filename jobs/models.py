import datetime
import re
from django import forms
from django.forms.widgets import DateInput
from django.core.exceptions import ValidationError
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from django.db import models
from django.shortcuts import get_object_or_404, render
from django.db.models import Avg
from .validators import validate_is_pdf
from ckeditor.fields import RichTextField


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
    username= models.CharField(max_length=30, blank=True)
    first_name=models.CharField(max_length=30, blank=True)
    last_name=models.CharField(max_length=30, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def get_short_name(self):
        return self.first_name
    
    def get_rating(self): 
        avg_rating = self.recipient_ratings.aggregate(Avg('rating'))['rating__avg'] 
        if avg_rating is not None: 
            return round(avg_rating, 2) 
        else: 
            return None
    
    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.first_name +" "+ self.last_name
        super().save(*args, **kwargs)


class Company(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    field = models.CharField(max_length=30, blank=True)
    description = RichTextField(blank=True, null=True)
    logo = models.ImageField(default='default_picture.png', upload_to='company_profile_images', blank=True)
    skills = ArrayField(models.CharField(null=True, blank=True, max_length=30), null=True, blank=True)
    instagram_link = models.URLField(max_length=200, blank=True) 
    linkedin_link = models.URLField(max_length=200, blank=True) 
    facebook_link = models.URLField(max_length=200, blank=True) 
    website_link = models.URLField(max_length=200, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def get_num_ratings(self):
        return Rating.objects.filter(recipient=self.user).count()

    def get_rating(self):
        return self.user.get_rating()
    
    def get_num_jobs_posted(self):
        return Job.objects.filter(company=self).count()

    def get_member_since(self):
        return self.created_at.strftime("%Y")

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = self.user.first_name
        if not self.field:
            self.field = self.user.last_name
        super().save(*args, **kwargs)

# class Skill(models.Model): 
#     name = models.CharField(default='m', max_length=50) 

#     def __str__(self):
#         return self.name


# class Freelancer(models.Model):
#     user = models.OneToOneField(CustomUser, on_delete=models.CASCADE) 
#     first_name = models.CharField(default='', max_length=20)
#     last_name = models.CharField(default='', max_length=20)
#     occupation = models.CharField(default='', max_length=20)
#     level = models.CharField(default='', max_length=15)
#     bio = RichTextField(blank=True, null=True)
#     photo = models.ImageField(default='default_picture.png', upload_to='freelancer_profile_images', blank=True)
#     skills = models.ManyToManyField(Skill) 
#     education_university = models.CharField(default='', max_length=30)
#     education_specialization = models.CharField(default='', max_length=30)
#     education_year_of_study = models.CharField(default='', max_length=20)
#     experience_position = models.CharField(default='', max_length=30)
#     experience_company_name = models.CharField(default='', max_length=30)
#     experience_work_duration = models.CharField(default='', max_length=20)
#     experience_description = models.TextField(default='')
#     created_at = models.DateTimeField(auto_now_add=True)
#     portfolio_link = models.URLField(blank=True)

#     def get_rating(self):
#         return self.user.get_rating()

class Skill(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

# class Position(models.Model):
#     name = models.CharField(default='', null=True, max_length=25) 
    
#     def __str__(self):
#         return self.name

class Freelancer(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE) 
    first_name = models.CharField(default='', max_length=20)
    last_name = models.CharField(default='', max_length=20)
    occupation = models.CharField(default='', max_length=20)
    level = models.CharField(default='', max_length=15)
    bio = RichTextField(blank=True, null=True)
    photo = models.ImageField(default='default_picture.png', upload_to='freelancer_profile_images', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    portfolio_link = models.URLField(blank=True)
    skills = models.ManyToManyField(Skill, blank=True)

    def get_num_ratings(self):
        return Rating.objects.filter(recipient=self.user).count()

    def get_rating(self):
        return self.user.get_rating()
    
    def save(self, *args, **kwargs):
        if not self.first_name:
            self.first_name = self.user.first_name
        if not self.last_name:
            self.last_name = self.user.last_name
        super().save(*args, **kwargs)


class Project(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    freelancer = models.ForeignKey(Freelancer, on_delete=models.CASCADE)
    link = models.URLField()
    platform = models.CharField(max_length=50)

    
class Education(models.Model):
    freelancer = models.ForeignKey(Freelancer, on_delete=models.CASCADE, related_name='educations')
    university = models.CharField(max_length=30)
    specialization = models.CharField(max_length=30)
    year_of_study = models.CharField(max_length=20)


class Experience(models.Model):
    freelancer = models.ForeignKey(Freelancer, on_delete=models.CASCADE, related_name='experiences')
    position = models.CharField(max_length=30)
    company_name = models.CharField(max_length=30)
    work_duration = models.CharField(max_length=20)
    description = models.TextField()


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
    description = RichTextField(blank=True, null=True) 
    file = models.FileField(upload_to='company_files/', validators=(validate_is_pdf,), blank=True) 
    category = models.ForeignKey(Category, on_delete=models.CASCADE) 
    skills = models.ManyToManyField(Skill, blank=True) 
    position = models.CharField(default='', max_length=20) 
    created_at = models.DateTimeField(auto_now_add=True) 
    company = models.ForeignKey(Company, on_delete=models.CASCADE) 
    is_active = models.BooleanField(default=True) 
    salary = models.PositiveIntegerField(null=True, blank=True) 
    timeline = models.DateField() 
    freelancer = models.ForeignKey(Freelancer, on_delete=models.SET_NULL, blank=True, null=True) 
    status = models.CharField(max_length=255, default='pending')

    def get_timeline_display(self):
        return self.timeline.strftime("%d.%m.%Y")
    
    def freelancer_has_applied(self, freelancer):
        return JobApplication.objects.filter(job=self, freelancer=freelancer).exists()
    

class JobApplication(models.Model): 
    job = models.ForeignKey(Job, on_delete=models.CASCADE) 
    freelancer = models.ForeignKey(Freelancer, on_delete=models.CASCADE) 
    status=models.CharField(max_length=20,default='pending')


class Submission(models.Model): 
    job = models.ForeignKey(Job, on_delete=models.CASCADE) 
    freelancer = models.ForeignKey(Freelancer, on_delete=models.CASCADE) 
    link = models.URLField(max_length=255) 
    file = models.FileField(upload_to='freelancer_files/', blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True) 
    order = models.IntegerField(default=0)  
    STATUS_CHOICES = [ 
        ('pending', 'Pending'), 
        ('accepted', 'Accepted'), 
        ('rejected', 'Rejected'), 
    ] 
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending') 
 
    def __str__(self): 
        return f'Submission for "{self.job.title}" by {self.freelancer.user.username}'


class Rating(models.Model): 
    RATING_CHOICES = ( 
        (1, '1 star'), 
        (2, '2 stars'), 
        (3, '3 stars'), 
        (4, '4 stars'), 
        (5, '5 stars'), 
    ) 
    job = models.ForeignKey(Job, on_delete=models.CASCADE) 
    reviewer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='reviewer_ratings') 
    recipient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='recipient_ratings') 
    rating = models.IntegerField(choices=RATING_CHOICES) 
    comment = models.TextField(blank=True) 
    created_at = models.DateTimeField(auto_now_add=True) 
 
    class Meta: 
        unique_together = ('job', 'reviewer', 'recipient')

    
class Chat(models.Model):
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='receiver')
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']