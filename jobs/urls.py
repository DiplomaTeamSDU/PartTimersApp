from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('edit_profile/<str:role>/', views.edit_profile, name='edit_profile'),
    path('', views.index, name='home'),
    path('job_post/', views.index, name='job_post'),
    path('job_search/', views.index, name='job_search'),
]