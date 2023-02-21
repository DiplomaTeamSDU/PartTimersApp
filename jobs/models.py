from django.db import models
from django.contrib.auth.models import User

class Company(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    logo = models.ImageField(upload_to='company_logos/', blank=True)

class Job(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    salary = models.PositiveIntegerField(null=True, blank=True)

class Freelancer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField()
    photo = models.ImageField(upload_to='photos')
    skills = models.TextField()
    education = models.TextField()
    experience = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    portfolio_link = models.URLField(blank=True)

