from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.core.paginator import Paginator
from .models import Evidence, LaboratoryTest
from .forms  import EvidenceForm, LabTestCreateForm, LabTestResultForm
from apps.core.decorators import not_viewer, lab_or_admin
from apps.core.middleware  import log_action


@login_required
def evidence_list(request):
    qs     = Evidence.objects.select_related('case', 'case__patient').all()
    status = request.GET.get('status', '')
    q      = request.GET.get('q', '')
    if status:
        qs = qs.filter(analysis_status=status)
    if q:
        qs = qs.filter(evidence_type__icontains=q) | qs.filter(barcode_number__icontains=q) | qs.filter(case__case_number__icontains=q)
    paginator = Paginator(qs.distinct(), 20)
    return render(request, 'evidence/list.html', {
        'page_obj': paginator.get_page(request.GET.get('page')),
        'status': status, 'q': q,
        'page_title': 'Evidence & Lab Tests', 'active_nav': 'evidence'})


@login_required
def barcode_lookup(request):
    """Lookup evidence by barcode — used by USB barcode scanner quick-search.
    GET ?bc=FMD12345678  → redirects to evidence detail if found
    GET ?bc=...&format=json → returns JSON (for AJAX)
    """
    bc = request.GET.get('bc', '').strip()
    if not bc:
        return redirect('evidence:list')

    try:
        ev = Evidence.objects.get(barcode_number=bc)
        if request.GET.get('format') == 'json':
            return JsonResponse({
                'found': True,
                'evidence_id':     ev.evidence_id,
                'evidence_number': ev.evidence_number,
                'evidence_type':   ev.evidence_type,
                'case_number':     ev.case.case_number,
                'patient_name':    ev.case.patient.full_name,
                'analysis_status': ev.analysis_status,
                'redirect_url':    f'/evidence/{ev.evidence_id}/detail/',
            })
        log_action(request.user, 'READ', 'Evidence', ev.evidence_id,
                   f'Barcode scan lookup: {bc}', request)
        return redirect('evidence:detail', pk=ev.evidence_id)
    except Evidence.DoesNotExist:
        if request.GET.get('format') == 'json':
            return JsonResponse({'found': False, 'barcode': bc})
        messages.error(request, f'No evidence found with barcode: {bc}')
        return redirect('evidence:list')


@login_required
def evidence_detail(request, pk):
    """Show evidence item + all its lab tests."""
    ev        = get_object_or_404(Evidence, pk=pk)
    lab_tests = ev.lab_tests.select_related('technician').order_by('-test_date')
    return render(request, 'evidence/detail.html', {
        'ev': ev, 'lab_tests': lab_tests,
        'page_title': f'Evidence {ev.evidence_number}', 'active_nav': 'evidence'})


@login_required
@not_viewer
def evidence_create(request):
    case_id = request.GET.get('case')
    initial = {}
    if case_id:
        from apps.cases.models import ForensicCase
        try:
            initial['case'] = ForensicCase.objects.get(pk=case_id)
        except ForensicCase.DoesNotExist:
            pass
    form = EvidenceForm(request.POST or None, initial=initial)
    if request.method == 'POST' and form.is_valid():
        ev = form.save()
        log_action(request.user, 'CREATE', 'Evidence', ev.evidence_id,
                   f'Barcode: {ev.barcode_number}', request)
        messages.success(request, f'Evidence {ev.evidence_number} added. Barcode: {ev.barcode_number}')
        return redirect('cases:detail', pk=ev.case.case_id)
    return render(request, 'evidence/form.html', {
        'form': form, 'action': 'Add Evidence',
        'page_title': 'New Evidence', 'active_nav': 'evidence'})


@login_required
@not_viewer
def evidence_edit(request, pk):
    ev   = get_object_or_404(Evidence, pk=pk)
    form = EvidenceForm(request.POST or None, instance=ev)
    if request.method == 'POST' and form.is_valid():
        form.save()
        log_action(request.user, 'UPDATE', 'Evidence', pk, '', request)
        messages.success(request, 'Evidence updated.')
        return redirect('evidence:detail', pk=pk)   # ← go to evidence detail, not case
    return render(request, 'evidence/form.html', {
        'form': form, 'ev': ev, 'action': 'Edit Evidence',
        'page_title': f'Edit {pk}', 'active_nav': 'evidence'})


@login_required
@lab_or_admin
def labtest_create(request, evidence_pk):
    evidence = get_object_or_404(Evidence, pk=evidence_pk)
    form = LabTestCreateForm(request.POST or None, initial={'evidence': evidence})
    if request.method == 'POST' and form.is_valid():
        lt = form.save()
        # Auto-update evidence status: Pending → InProgress
        if evidence.analysis_status == 'Pending':
            evidence.analysis_status = 'InProgress'
            evidence.save(update_fields=['analysis_status'])
        log_action(request.user, 'CREATE', 'LaboratoryTest', lt.test_id,
                   f'Evidence: {evidence.evidence_number}', request)
        messages.success(request, f'Lab test {lt.test_id} opened for {evidence.evidence_number}. Lab technician can now enter results.')
        return redirect('evidence:detail', pk=evidence_pk)
    return render(request, 'evidence/labtest_form.html', {
        'form': form, 'evidence': evidence,
        'action': 'Open Lab Test',
        'form_type': 'create',
        'page_title': 'New Lab Test', 'active_nav': 'evidence'})


@login_required
@lab_or_admin
def labtest_enter_results(request, pk):
    """Lab technician enters test results and marks status."""
    lt   = get_object_or_404(LaboratoryTest, pk=pk)
    form = LabTestResultForm(request.POST or None, instance=lt)
    if request.method == 'POST' and form.is_valid():
        lt = form.save()
        # Auto-update evidence analysis_status based on all tests
        ev = lt.evidence
        all_tests   = ev.lab_tests.all()
        total       = all_tests.count()
        completed   = all_tests.filter(test_status='Completed').count()
        failed      = all_tests.filter(test_status='Failed').count()
        in_progress = all_tests.filter(test_status='InProgress').count()

        if completed == total and total > 0:
            ev.analysis_status = 'Completed'
            status_msg = f'All {total} tests completed. Evidence {ev.evidence_number} marked Completed.'
        elif failed > 0 and (completed + failed) == total:
            ev.analysis_status = 'Failed'
            status_msg = f'Evidence {ev.evidence_number} marked Failed ({failed} test(s) failed).'
        elif in_progress > 0 or completed > 0:
            ev.analysis_status = 'InProgress'
            status_msg = 'Results saved.'
        else:
            status_msg = 'Results saved.'
        ev.save(update_fields=['analysis_status'])

        log_action(request.user, 'UPDATE', 'LaboratoryTest', pk,
                   f'Results entered. Status: {lt.test_status}', request)
        messages.success(request, status_msg)
        return redirect('evidence:detail', pk=lt.evidence.evidence_id)
    return render(request, 'evidence/labtest_form.html', {
        'form': form, 'lt': lt, 'evidence': lt.evidence,
        'action': 'Enter Test Results',
        'form_type': 'results',
        'page_title': f'Results — {pk}', 'active_nav': 'evidence'})


@login_required
@lab_or_admin
def labtest_edit(request, pk):
    lt   = get_object_or_404(LaboratoryTest, pk=pk)
    # Decide which form based on whether results already exist
    if lt.test_result or lt.test_status in ('Completed', 'Failed', 'InProgress'):
        FormClass = LabTestResultForm
        action    = 'Update Test Results'
    else:
        FormClass = LabTestCreateForm
        action    = 'Edit Lab Test'
    form = FormClass(request.POST or None, instance=lt)
    if request.method == 'POST' and form.is_valid():
        lt = form.save()
        log_action(request.user, 'UPDATE', 'LaboratoryTest', pk, '', request)
        messages.success(request, 'Lab test updated.')
        return redirect('evidence:detail', pk=lt.evidence.evidence_id)
    return render(request, 'evidence/labtest_form.html', {
        'form': form, 'lt': lt, 'evidence': lt.evidence,
        'action': action,
        'form_type': 'edit',
        'page_title': f'Edit {pk}', 'active_nav': 'evidence'})
