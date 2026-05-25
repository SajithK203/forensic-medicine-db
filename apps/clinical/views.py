from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .models import ClinicalExamination
from .forms  import ClinicalExaminationForm
from apps.core.decorators import doctor_or_admin
from apps.core.middleware  import log_action

@login_required
def exam_list(request):
    qs = ClinicalExamination.objects.select_related('case','doctor').all()
    paginator = Paginator(qs, 20)
    return render(request, 'clinical/list.html', {
        'page_obj': paginator.get_page(request.GET.get('page')),
        'page_title': 'Clinical Examinations', 'active_nav': 'clinical'})

@login_required
@doctor_or_admin
def exam_create(request):
    form = ClinicalExaminationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        exam = form.save()
        log_action(request.user,'CREATE','ClinicalExamination',exam.exam_id,'',request)
        messages.success(request, f'Examination {exam.exam_id} recorded.')
        return redirect('cases:detail', pk=exam.case.case_id)
    return render(request, 'clinical/form.html', {
        'form': form, 'action': 'Record Clinical Examination',
        'page_title': 'New Examination', 'active_nav': 'clinical'})

@login_required
@doctor_or_admin
def exam_edit(request, pk):
    exam = get_object_or_404(ClinicalExamination, pk=pk)
    form = ClinicalExaminationForm(request.POST or None, instance=exam)
    if request.method == 'POST' and form.is_valid():
        form.save()
        log_action(request.user,'UPDATE','ClinicalExamination',pk,'',request)
        messages.success(request, 'Examination updated.')
        return redirect('cases:detail', pk=exam.case.case_id)
    return render(request, 'clinical/form.html', {
        'form': form, 'exam': exam, 'action': 'Edit Examination',
        'page_title': f'Edit {pk}', 'active_nav': 'clinical'})
