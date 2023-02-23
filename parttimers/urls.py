from django.contrib import admin
from django.urls import include, path
from jobs import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('jobs/', include('jobs.urls')),
    path('', views.index),
]