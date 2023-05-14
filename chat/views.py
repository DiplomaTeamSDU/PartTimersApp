from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

# Create your views here.
from chat.models import Thread
from jobs.models import Freelancer


@login_required
def messages_page(request):
    threads = Thread.objects.by_user(user=request.user).prefetch_related('chatmessage_thread').order_by('timestamp')
    context = {
        'Threads': threads
    }
    return render(request, 'messages.html', context)

@login_required
def start_chat(request, freelancer_id):

    company = request.user

    freelancer = get_object_or_404(Freelancer, id=freelancer_id)


    thread = Thread.objects.filter(Q(first_person=company, second_person=freelancer.user) | Q(first_person=freelancer.user, second_person=company))

    if thread.exists():
        
        return redirect('messages_page')

    thread = Thread.objects.create(first_person=company, second_person=freelancer.user)

    return redirect('messages_page')
