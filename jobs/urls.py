from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('company_profile/', views.profile, name='company_profile'),
    path('freelancer_profile/', views.profile, name='freelancer_profile'),
    path('', views.index, name='home'),
    path('job_post/', views.index, name='job_post'),
    path('job_search/', views.index, name='job_search'),
]