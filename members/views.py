from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from . forms import RegisterUserForm
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from todo.tasks import signupuser


# Login user and authentication
def access_granting(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(
                request, (f'{username} welcome to your todo list!'))
            return redirect('home')
        else:
            messages.success(request, ('''
            Sorry your username or password does not match!.
            Please enter a valid username or password and try again
            Thank you'''))
            return redirect('granted',)
    else:
        return render(request, 'members/login.html', {})


# Logout user
def logout_user(request):
    messages.success(request, ('Logout successful!'))
    logout(request)
    return redirect('/')


def signup(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        from_email = settings.EMAIL_HOST_USER
        if form.is_valid():
            # save form in the memory not in database
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            # to get the domain of the current site
            current_site = get_current_site(request)
            mail_subject = 'Activation link has been sent to your email id'
            message = render_to_string('members/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            receiver = [to_email]
            # celery to handle task
            signupuser.delay(message, to_email, from_email, mail_subject)
            return HttpResponse('Please confirm your email address to complete the registration')
    else:
        form = RegisterUserForm()
    return render(request, 'members/register.html', {'form': form})


def activate(request, uidb64, token):
    model = User
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = model.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')
