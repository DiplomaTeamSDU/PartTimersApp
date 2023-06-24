from django.urls import path
from . import views
urlpatterns = [
    path('', views.messages_page,name='messages_page'),
    path('start-chat/<int:freelancer_id>/', views.start_chat, name='start_chat'),
]
