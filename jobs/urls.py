from django.urls import path
from . import views
from .views import (
    apply_to_job,
    register,
    login_view,
    logout,
    profile,
    edit_profile,
    post_job,
    company_dashboard,
    view_job,
    view_jobs
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout, name='logout'),
    path('profile/', profile, name='profile'),
    path('edit_profile/<str:role>/', edit_profile, name='edit_profile'),
    path('', views.home, name='home'),
    path('post_job/', post_job, name='post_job'),
    path('company_dashboard/',company_dashboard,name='company_dashboard'),
    path('jobs/', view_jobs, name='view_jobs'),
    path('job/<int:job_id>/', view_job, name='view_job'),
    path('job/<int:job_id>/select_freelancer/<int:application_id>/', views.select_freelancer, name='select_freelancer'),
    path('freelancer/<int:freelancer_id>/', views.view_freelancer, name='view_freelancer'),
    path('job/<int:job_id>/', view_job, name='view_job'),
    path('apply_to_job/<int:job_id>/', apply_to_job, name='apply_to_job'),
    path('job_search/', views.home, name='job_search'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]