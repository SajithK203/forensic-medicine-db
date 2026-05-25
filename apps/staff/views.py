from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Staff, Doctor
from .forms  import StaffForm, DoctorForm
from apps.core.decorators import admin_required
from apps.core.middleware  import log_action

@login_required
@admin_required
def staff_list(request):
    qs = Staff.objects.all()
    paginator = Paginator(qs, 20)
    return render(request, 'staff/list.html', {
        'page_obj': paginator.get_page(request.GET.get('page')),
        'page_title': 'Staff Management', 'active_nav': 'staff'})

@login_required
@admin_required
def staff_create(request):
    form = StaffForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        s = form.save()
        log_action(request.user,'CREATE','Staff',s.staff_id,'',request)
        messages.success(request, f'Staff {s.full_name} added. ID: {s.staff_id}')
        return redirect('staff:list')
    return render(request, 'staff/form.html', {
        'form': form, 'action': 'Add Staff Member',
        'page_title': 'New Staff', 'active_nav': 'staff'})

@login_required
@admin_required
def staff_edit(request, pk):
    s    = get_object_or_404(Staff, pk=pk)
    form = StaffForm(request.POST or None, instance=s)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Staff updated.')
        return redirect('staff:list')
    return render(request, 'staff/form.html', {
        'form': form, 'staff': s, 'action': 'Edit Staff',
        'page_title': f'Edit {s.full_name}', 'active_nav': 'staff'})

@login_required
@admin_required
def doctor_create(request):
    form = DoctorForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        d = form.save()
        log_action(request.user,'CREATE','Doctor',d.doctor_id,'',request)
        messages.success(request, f'Doctor {d.full_name} added. ID: {d.doctor_id}')
        return redirect('staff:list')
    return render(request, 'staff/form.html', {
        'form': form, 'action': 'Add Doctor',
        'page_title': 'New Doctor', 'active_nav': 'staff'})
