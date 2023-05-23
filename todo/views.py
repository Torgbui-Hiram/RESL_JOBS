from __future__ import absolute_import, unicode_literals
from django.shortcuts import render, redirect
from .models import PendingJob, DepartmentHead
from .forms import PendingJobForm
from django.contrib import messages
from django.core.mail import send_mail
from decouple import config
from todo.tasks import send_reminder, get_pending_job
from django.utils import timezone
from django.shortcuts import get_object_or_404


# Send reminder email to all department heads
def reminder(request):
    send_reminder.apply_async(countdown=5)
    return redirect('home')


# submit an action when job is completed
def sub_action(request):
    form = PendingJobForm(instance=PendingJob)
    if request.method == "POST":
        action = request.POST.get('completed')
        if action == 'on':
            job = PendingJob.job_status = 'True'
            pass
        else:
            pass
    return render(request, 'close_job.html', {'form': form})


# Homepage
def home(request):
    get_pending_job(request)
    all_email = DepartmentHead.objects.values_list('email')
    recipient_list = []
    for each in all_email:
        recipient_list.append(list(each)[0])
    if request.method == "POST":
        # Search a word from a form when the form is submitted
        search = request.POST.get('search_value')
        job = PendingJob.objects.filter(
            station__icontains=search)
        return render(request, 'search.html', {})
    else:
        pending = PendingJob.objects.all()
    return render(request, 'index.html', {'pending': pending, })


# Add pending jobs
def add_job(request):
    if request.method == "POST":
        form = PendingJobForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            messages.success(
                request, 'There was an errror with your form, try agin')
            return redirect('add_job')
    form = PendingJobForm()
    return render(request, 'pendingjobform.html', {'form': form})


# View pending job details
def view_details(request, id):
    if request.method == "POST":
        status = request.POST.get('toggler-1')
        # Create an instance of the job
        form = PendingJobForm(instance=PendingJob)

        # Get the selected job from database
        job = PendingJob.objects.get(pk=id)

        # Negate the the state of the jobjob = PendingJob.job_status = 'True'
        if status:
            job.job_status = not job.job_status
            job.save()
        else:
            job.job_status = job.job_status
    detail = PendingJob.objects.get(pk=id)
    return render(request, 'job_details.html', {'detail': detail})
