import re
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

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


# class Company(models.Model):
#     user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
#     name = models.CharField(max_length=255)
#     description = models.TextField(blank=True,)
#     logo = models.ImageField(upload_to='company_logos/', blank=True)

class Company(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    logo = models.ImageField(default='default_picture.png', upload_to='company_profile_images', blank=True)


class Skill(models.Model):
    name = models.CharField(max_length=255)

class Freelancer(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE) 
    first_name = models.CharField(default='', max_length=20)
    last_name = models.CharField(default='', max_length=20)
    occupation = models.CharField(default='', max_length=20)
    bio = models.TextField()
    photo = models.ImageField(default='default_picture.png', upload_to='freelancer_profile_images', blank=True)
    # skills = models.TextField()
    education = models.TextField()
    experience = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    portfolio_link = models.URLField(blank=True)

class Category(models.Model):
    name = models.CharField(max_length=255) 
    
    def __str__(self):
        return self.name


class TimeInput(forms.TextInput):

    def get_context(self, name, value, attrs):
        if value:
            # Convert time from seconds to HH:MM:SS format
            hours, remainder = divmod(int(value), 3600)
            minutes, seconds = divmod(remainder, 60)
            value = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        return super().get_context(name, value, attrs)


class TimeField(forms.CharField):
    # Check that the value matches the format HH:MM:SS
    def validate(self, value):
        super().validate(value)
        if value is not None and isinstance(value, (str, bytes)) and not re.match(r"^\d{1,2}:\d{2}:\d{2}$", value):
            raise ValidationError("Invalid time format. Use HH:MM:SS.")

    def to_python(self, value):
        if value:
            try:
                hours, minutes, seconds = map(int, value.split(":"))
                if not (0 <= hours <= 72 and 0 <= minutes <= 59 and 0 <= seconds <= 59):
                    raise ValidationError("Invalid time range.")
                return hours * 3600 + minutes * 60 + seconds
            except ValueError:
                pass
        return value

class Job(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    salary = models.PositiveIntegerField(null=True, blank=True)
    timeline = models.PositiveIntegerField(default=0)


    def get_timeline_display(self):
        # Convert timeline from seconds to HH:MM:SS format
        hours, remainder = divmod(int(self.timeline), 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

