from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Evidence, LaboratoryTest
from .forms  import EvidenceForm, LabTestForm
from apps.core.decorators import not_viewer, lab_or_admin
from apps.core.middleware  import log_action

@login_required
def evidence_list(request):
    qs = Evidence.objects.select_related('case').all()
    status = request.GET.get('status','')
    if status: qs = qs.filter(analysis_status=status)
    paginator = Paginator(qs, 20)
    return render(request, 'evidence/list.html', {
        'page_obj': paginator.get_page(request.GET.get('page')),
        'status': status, 'page_title': 'Evidence', 'active_nav': 'evidence'})

@login_required
@not_viewer
def evidence_create(request):
    form = EvidenceForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        ev = form.save()
        log_action(request.user,'CREATE','Evidence',ev.evidence_id,
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
        log_action(request.user,'UPDATE','Evidence',pk,'',request)
        messages.success(request, 'Evidence updated.')
        return redirect('cases:detail', pk=ev.case.case_id)
    return render(request, 'evidence/form.html', {
        'form': form, 'ev': ev, 'action': 'Edit Evidence',
        'page_title': f'Edit {pk}', 'active_nav': 'evidence'})

@login_required
@lab_or_admin
def labtest_create(request, evidence_pk):
    evidence = get_object_or_404(Evidence, pk=evidence_pk)
    form = LabTestForm(request.POST or None, initial={'evidence': evidence})
    if request.method == 'POST' and form.is_valid():
        lt = form.save()
        log_action(request.user,'CREATE','LaboratoryTest',lt.test_id,'',request)
        messages.success(request, f'Lab test {lt.test_id} created.')
        return redirect('evidence:list')
    return render(request, 'evidence/form.html', {
        'form': form, 'evidence': evidence, 'action': 'Add Lab Test',
        'page_title': 'New Lab Test', 'active_nav': 'evidence'})
