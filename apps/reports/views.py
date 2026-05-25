from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.utils import timezone
from .models import CourtReport
from .forms  import CourtReportForm
from apps.core.decorators import doctor_or_admin, not_viewer
from apps.core.middleware  import log_action

@login_required
def report_list(request):
    qs = CourtReport.objects.select_related('case','doctor').all()
    status = request.GET.get('status','')
    rtype  = request.GET.get('report_type','')
    if status: qs = qs.filter(report_status=status)
    if rtype:  qs = qs.filter(report_type=rtype)
    paginator = Paginator(qs, 20)
    return render(request, 'reports/list.html', {
        'page_obj': paginator.get_page(request.GET.get('page')),
        'status': status, 'report_type': rtype,
        'page_title': 'Court Reports', 'active_nav': 'reports'})

@login_required
@doctor_or_admin
def report_create(request):
    form = CourtReportForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        rpt = form.save()
        log_action(request.user,'CREATE','CourtReport',rpt.report_id,'',request)
        messages.success(request, f'Report {rpt.report_id} created.')
        return redirect('reports:list')
    return render(request, 'reports/form.html', {
        'form': form, 'action': 'Create Court Report',
        'page_title': 'New Report', 'active_nav': 'reports'})

@login_required
@doctor_or_admin
def report_edit(request, pk):
    rpt  = get_object_or_404(CourtReport, pk=pk)
    form = CourtReportForm(request.POST or None, instance=rpt)
    if request.method == 'POST' and form.is_valid():
        form.save()
        log_action(request.user,'UPDATE','CourtReport',pk,'',request)
        messages.success(request, 'Report updated.')
        return redirect('reports:list')
    return render(request, 'reports/form.html', {
        'form': form, 'rpt': rpt, 'action': 'Edit Report',
        'page_title': f'Edit {pk}', 'active_nav': 'reports'})

@login_required
@doctor_or_admin
def report_submit(request, pk):
    rpt = get_object_or_404(CourtReport, pk=pk)
    if rpt.report_status not in ['Generated','Reviewed']:
        messages.error(request, 'Only Generated or Reviewed reports can be submitted.')
    else:
        rpt.report_status = 'Submitted'
        rpt.submitted_at  = timezone.now()
        rpt.approved_by   = request.user.get_full_name() or request.user.username
        rpt.save()
        log_action(request.user,'SUBMIT','CourtReport',pk,f'Submitted to {rpt.court_name}',request)
        messages.success(request, f'Report {pk} submitted to {rpt.court_name}.')
    return redirect('reports:list')
