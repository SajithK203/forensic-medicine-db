from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages


def role_required(*roles):
    """Decorator that restricts a view to users with one of the given roles."""
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('accounts:login')
            if request.user.role not in roles:
                messages.error(request, 'You do not have permission to access this page.')
                return redirect('core:dashboard')
            return view_func(request, *args, **kwargs)
        return _wrapped
    return decorator


def admin_required(view_func):
    return role_required('Administrator')(view_func)


def doctor_or_admin(view_func):
    return role_required('Doctor', 'Administrator')(view_func)


def lab_or_admin(view_func):
    return role_required('LabTechnician', 'Administrator')(view_func)


def not_viewer(view_func):
    return role_required('Doctor', 'LabTechnician', 'Administrator')(view_func)
