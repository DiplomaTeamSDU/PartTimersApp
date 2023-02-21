from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('profile/', views.profile, name='profile'),
    #path('job-post/', views.job_post, name='job_post'),
    #path('job-search/', views.job_search, name='job_search'),
]