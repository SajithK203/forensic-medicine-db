from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q

from .models import Patient
from .forms  import PatientForm
from apps.core.decorators  import not_viewer
from apps.core.middleware  import log_action


@login_required
def patient_list(request):
    qs = Patient.objects.all()
    q  = request.GET.get('q', '').strip()
    if q:
        qs = qs.filter(
            Q(full_name__icontains=q) |
            Q(nic_passport__icontains=q) |
            Q(district__icontains=q)
        )
    gender   = request.GET.get('gender', '')
    district = request.GET.get('district', '')
    if gender:   qs = qs.filter(gender=gender)
    if district: qs = qs.filter(district__icontains=district)

    paginator = Paginator(qs, 20)
    page_obj  = paginator.get_page(request.GET.get('page'))

    return render(request, 'patients/list.html', {
        'page_obj':   page_obj,
        'q':          q,
        'gender':     gender,
        'district':   district,
        'page_title': 'Patients',
        'active_nav': 'patients',
    })


@login_required
def patient_detail(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    cases   = patient.cases.select_related('doctor').order_by('-created_at')
    log_action(request.user, 'VIEW', 'Patient', pk, f'Viewed patient {pk}', request)
    return render(request, 'patients/detail.html', {
        'patient':    patient,
        'cases':      cases,
        'page_title': f'Patient — {patient.full_name}',
        'active_nav': 'patients',
    })


@login_required
@not_viewer
def patient_create(request):
    form = PatientForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        patient = form.save()
        log_action(request.user, 'CREATE', 'Patient', patient.patient_id,
                   f'Created patient {patient.full_name}', request)
        messages.success(request, f'Patient {patient.full_name} registered. ID: {patient.patient_id}')
        return redirect('patients:detail', pk=patient.patient_id)
    return render(request, 'patients/form.html', {
        'form':       form,
        'action':     'Register New Patient',
        'page_title': 'New Patient',
        'active_nav': 'patients',
    })


@login_required
@not_viewer
def patient_edit(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    form    = PatientForm(request.POST or None, request.FILES or None, instance=patient)
    if request.method == 'POST' and form.is_valid():
        form.save()
        log_action(request.user, 'UPDATE', 'Patient', pk, f'Updated patient {pk}', request)
        messages.success(request, 'Patient record updated.')
        return redirect('patients:detail', pk=pk)
    return render(request, 'patients/form.html', {
        'form':       form,
        'patient':    patient,
        'action':     'Edit Patient',
        'page_title': f'Edit — {patient.full_name}',
        'active_nav': 'patients',
    })
