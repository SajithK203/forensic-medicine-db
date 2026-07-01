from django.contrib.auth.views import LogoutView
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods

from apps.core.middleware import log_action
from .forms import LoginForm, ProfileEditForm


@require_http_methods(['GET', 'POST'])
def login_view(request):
    if request.user.is_authenticated:
        return redirect('core:dashboard')

    form = LoginForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user     = authenticate(request, username=username, password=password)

        if user is None:
            messages.error(request, 'Invalid username or password.')
        elif user.is_locked:
            messages.error(request, 'Your account is locked. Contact the administrator.')
        elif not user.is_active:
            messages.error(request, 'Your account is inactive.')
        else:
            # Reset failed attempts on successful login
            user.login_attempts = 0
            user.last_login_ip  = request.META.get('REMOTE_ADDR')
            user.save(update_fields=['login_attempts', 'last_login_ip', 'last_login'])
            login(request, user)
            log_action(user, 'LOGIN', details=f'Login from {user.last_login_ip}', request=request)
            messages.success(request, f'Welcome back, {user.get_full_name() or user.username}!')
            return redirect(request.GET.get('next', 'core:dashboard'))

    return render(request, 'accounts/login.html', {
        'form':       form,
        'page_title': 'Sign In',
    })


def logout_view(request):
    if request.user.is_authenticated:
        log_action(request.user, 'LOGOUT', request=request)
    from django.contrib.auth import logout
    logout(request)
    messages.info(request, 'You have been signed out.')
    return redirect('accounts:login')


@login_required
def profile_view(request):
    from apps.core.models import ActivityLog
    recent_activity = ActivityLog.objects.filter(user=request.user).order_by('-logged_at')[:10]
    return render(request, 'accounts/profile.html', {
        'page_title':      'My Profile',
        'recent_activity': recent_activity,
    })


@login_required
def edit_profile_view(request):
    user = request.user
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, user=user)
        if form.is_valid():
            cd = form.cleaned_data

            # Update personal info
            user.first_name = cd['first_name']
            user.last_name  = cd['last_name']
            user.email      = cd['email']

            # Optional password change
            if cd.get('new_password'):
                user.set_password(cd['new_password'])
                messages.success(request, 'Password changed successfully. Please log in again.')
                user.save()
                log_action(user, 'UPDATE', model_name='CustomUser',
                           details='Profile updated + password changed', request=request)
                from django.contrib.auth import update_session_auth_hash
                update_session_auth_hash(request, user)   # keep user logged in
            else:
                user.save(update_fields=['first_name', 'last_name', 'email'])
                log_action(user, 'UPDATE', model_name='CustomUser',
                           details='Profile information updated', request=request)
                messages.success(request, 'Profile updated successfully.')

            return redirect('accounts:profile')
    else:
        form = ProfileEditForm(user=user)

    return render(request, 'accounts/edit_profile.html', {
        'page_title': 'Edit Profile',
        'form':       form,
    })
