from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q

from .models  import ForensicCase
from .forms   import CaseForm, CaseStatusForm
from apps.core.decorators import not_viewer, doctor_or_admin
from apps.core.middleware  import log_action


@login_required
def case_list(request):
    qs = ForensicCase.objects.select_related('patient', 'doctor').all()
    q        = request.GET.get('q', '').strip()
    status   = request.GET.get('status', '')
    case_type = request.GET.get('case_type', '')
    priority = request.GET.get('priority', '')

    if q:
        qs = qs.filter(
            Q(case_number__icontains=q) |
            Q(patient__full_name__icontains=q) |
            Q(police_report_no__icontains=q)
        )
    if status:    qs = qs.filter(case_status=status)
    if case_type: qs = qs.filter(case_type=case_type)
    if priority:  qs = qs.filter(priority=priority)

    paginator = Paginator(qs, 20)
    page_obj  = paginator.get_page(request.GET.get('page'))

    return render(request, 'cases/list.html', {
        'page_obj':   page_obj,
        'q':          q,
        'status':     status,
        'case_type':  case_type,
        'priority':   priority,
        'page_title': 'Cases',
        'active_nav': 'cases',
    })


@login_required
def case_detail(request, pk):
    case = get_object_or_404(
        ForensicCase.objects.select_related('patient', 'doctor'), pk=pk
    )
    log_action(request.user, 'VIEW', 'ForensicCase', pk, f'Viewed case {pk}', request)
    return render(request, 'cases/detail.html', {
        'case':          case,
        'examinations':  case.clinical_examinations.select_related('doctor').all(),
        'postmortem':    getattr(case, 'postmortem', None),
        'evidence_items': case.evidence_items.all(),
        'court_reports': case.court_reports.all(),
        'page_title':    f'Case — {case.case_number}',
        'active_nav':    'cases',
    })


@login_required
@not_viewer
def case_create(request):
    form = CaseForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        case = form.save()
        log_action(request.user, 'CREATE', 'ForensicCase', case.case_id,
                   f'Created case {case.case_number}', request)
        messages.success(request, f'Case {case.case_number} created.')
        return redirect('cases:detail', pk=case.case_id)
    return render(request, 'cases/form.html', {
        'form':       form,
        'action':     'Open New Case',
        'page_title': 'New Case',
        'active_nav': 'cases',
    })


@login_required
@not_viewer
def case_edit(request, pk):
    case = get_object_or_404(ForensicCase, pk=pk)
    form = CaseForm(request.POST or None, instance=case)
    if request.method == 'POST' and form.is_valid():
        form.save()
        log_action(request.user, 'UPDATE', 'ForensicCase', pk, f'Updated case {pk}', request)
        messages.success(request, 'Case updated.')
        return redirect('cases:detail', pk=pk)
    return render(request, 'cases/form.html', {
        'form':       form,
        'case':       case,
        'action':     'Edit Case',
        'page_title': f'Edit — {case.case_number}',
        'active_nav': 'cases',
    })


@login_required
@doctor_or_admin
def case_update_status(request, pk):
    case = get_object_or_404(ForensicCase, pk=pk)
    form = CaseStatusForm(request.POST or None, instance=case)
    if request.method == 'POST' and form.is_valid():
        try:
            form.save()
            log_action(request.user, 'UPDATE', 'ForensicCase', pk,
                       f'Status changed to {case.case_status}', request)
            messages.success(request, f'Case status updated to {case.case_status}.')
            return redirect('cases:detail', pk=pk)
        except Exception as e:
            messages.error(request, f'Failed to update case status: {str(e)}')
    return render(request, 'cases/form.html', {
        'form':       form,
        'case':       case,
        'action':     'Update Status',
        'page_title': f'Status — {case.case_number}',
        'active_nav': 'cases',
    })
