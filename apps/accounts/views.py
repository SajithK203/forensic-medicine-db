from django.contrib.auth.views import LogoutView
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.views.decorators.http import require_http_methods

from apps.core.middleware import log_action
from .forms import LoginForm


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
