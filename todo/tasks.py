from __future__ import absolute_import, unicode_literals
from decouple import config
from celery import Celery
from todo.models import DepartmentHead, PendingJob
from celery import shared_task
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.http import request
from members.forms import RegisterUserForm
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from members.tokens import account_activation_token
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate


def get_pending_job(request):
    every_station = []
    jobs = PendingJob.objects.filter(job_status='False')
    trial = PendingJob.objects.values_list('station', flat=True)
    for names in trial:
        every_station.append(names)
    return trial


@shared_task
def signupuser(message, to_email, from_email, mail_subject):
    receiver = [to_email]
    send_mail(mail_subject, message, from_email,
              receiver, fail_silently=False)
    status = {'state': 'Mail sent'}
    return status.get('state')


# Send reminder email to all department heads
@shared_task
def send_reminder():
    # Check the pending job list for uncompleted jobs
    jobs = list(PendingJob.objects.filter(
        job_status='False'))
    # Get all emails for department heads
    all_email = DepartmentHead.objects.values_list('email')

    # Email
    subject = 'Reminder on puma pending jobs'
    every_job = []
    for job in jobs:
        every_job.append(job.station)
    message = f'''
    These are the list of pending jobs we have for puma stations
    kindly follow up as to what we need to have them complete and
    close from the portal.

    ********* NOTICE ********
    {str(every_job)}
    Thank you.

    '''
    from_email = config('EMAIL_HOST_USER')

    # Looping through all the email from departments
    recipient_list = []
    for each in all_email:
        recipient_list.append(list(each)[0])

    # Sending the email
        send_mail(subject, message, from_email,
                  recipient_list, fail_silently=False)

    status = {'state': 'Mail sent'}
    return status.get('state')
