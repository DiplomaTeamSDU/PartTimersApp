from django.urls import path
from . import views
from .views import (
    register,
    login_view,
    logout,
    profile,
    edit_profile,
    post_job,
    company_dashboard,
    apply_to_job,
    view_job,
    view_jobs,
    see_applications,
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout, name='logout'),
    path('password_reset/', PasswordResetView.as_view(template_name='sign/password_reset_form.html'), name='password_reset'), 
    path('password_reset/done/', PasswordResetDoneView.as_view(template_name='sign/password_reset_done_form.html'), name='password_reset_done'), 
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='sign/password_reset_confirm.html'), name='password_reset_confirm'), 
    path('reset/done/', PasswordResetCompleteView.as_view(template_name='sign/password_reset_complete.html'), name='password_reset_complete'),
    path('profile/', profile, name='profile'),
    path('edit_profile/<str:role>/', edit_profile, name='edit_profile'),
    path('post_job/', post_job, name='post_job'),
    path('edit_job/<int:job_id>/', views.edit_job, name='edit_job'),
    path('edit_skills/', views.edit_skills, name='edit_skills'),
    path('company_dashboard/',company_dashboard,name='company_dashboard'),
    path('find_freelancer/', views.find_freelancer, name='find_freelancer'),
    path('jobs/', views.view_jobs, name='view_jobs'),
    path('job/<int:job_id>/', view_job, name='view_job'),
    path('job/<int:job_id>/apply/', views.apply_to_job, name='apply_to_job'),
    # path('job/<int:job_id>/submit_work/', views.submit_work, name='submit_work'), 
    path('view_submission/<int:submission_id>', views.view_submission, name='view_submission'), 
    path('accept_submission/<int:submission_id>/', views.accept_submission, name='accept_submission'),
    path('job/<int:job_id>/select_freelancer/<int:application_id>/', views.select_freelancer, name='select_freelancer'),
    path('post_project/', views.post_project, name='post_project'),
    path('freelancer/<int:freelancer_id>/', views.view_freelancer, name='view_freelancer'),
    path('apply_to_job/<int:job_id>/', apply_to_job, name='apply_to_job'),
    path('applications/', see_applications, name='applications'),
    path('active_projects/', views.active_projects, name='active_projects'),
    path('job_search/', views.home, name='job_search'),
    path('rate/<int:job_id>/<int:recipient_id>/', views.rate, name='rate'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)