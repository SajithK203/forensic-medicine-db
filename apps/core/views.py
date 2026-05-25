from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta

from apps.cases.models    import ForensicCase
from apps.patients.models  import Patient
from apps.evidence.models  import Evidence
from apps.reports.models   import CourtReport
from apps.postmortem.models import Postmortem
from apps.core.models      import ActivityLog


@login_required
def dashboard(request):
    now  = timezone.now()
    year = now.year

    # ── KPI counts ────────────────────────────────────────────────────────────
    total_cases      = ForensicCase.objects.count()
    active_cases     = ForensicCase.objects.exclude(case_status__in=['Closed', 'Archived']).count()
    total_patients   = Patient.objects.count()
    pending_reports  = CourtReport.objects.filter(report_status__in=['Draft', 'Generated', 'Reviewed']).count()
    pending_evidence = Evidence.objects.filter(analysis_status='Pending').count()

    # ── Recent cases (last 10) ────────────────────────────────────────────────
    recent_cases = (
        ForensicCase.objects
        .select_related('patient', 'doctor')
        .order_by('-created_at')[:10]
    )

    # ── Monthly case data for chart (last 12 months) ──────────────────────────
    months_labels  = []
    months_clinical = []
    months_autopsy  = []
    for i in range(11, -1, -1):
        dt    = now - timedelta(days=i * 30)
        label = dt.strftime('%b %Y')
        months_labels.append(label)
        months_clinical.append(
            ForensicCase.objects.filter(
                incident_date__year=dt.year,
                incident_date__month=dt.month,
                case_type='Clinical Forensic'
            ).count()
        )
        months_autopsy.append(
            ForensicCase.objects.filter(
                incident_date__year=dt.year,
                incident_date__month=dt.month,
                case_type='Autopsy'
            ).count()
        )

    # ── Case type distribution (doughnut) ─────────────────────────────────────
    type_data = (
        ForensicCase.objects
        .values('case_type')
        .annotate(count=Count('case_id'))
    )

    # ── Death type breakdown (bar chart) ──────────────────────────────────────
    death_data = (
        Postmortem.objects
        .values('death_type')
        .annotate(count=Count('postmortem_id'))
        .order_by('-count')
    )

    # ── Overdue cases (>30 days, not closed) ──────────────────────────────────
    overdue_threshold = now - timedelta(days=30)
    overdue_cases = (
        ForensicCase.objects
        .filter(incident_date__lt=overdue_threshold)
        .exclude(case_status__in=['Completed', 'Closed', 'Archived', 'Submitted'])
        .select_related('patient', 'doctor')
        .order_by('incident_date')[:5]
    )

    # ── Recent activity log ───────────────────────────────────────────────────
    recent_logs = ActivityLog.objects.select_related('user').order_by('-logged_at')[:15]

    context = {
        'total_cases':       total_cases,
        'active_cases':      active_cases,
        'total_patients':    total_patients,
        'pending_reports':   pending_reports,
        'pending_evidence':  pending_evidence,
        'recent_cases':      recent_cases,
        'overdue_cases':     overdue_cases,
        'recent_logs':       recent_logs,
        # Chart data (as Python lists — serialised in template)
        'months_labels':     months_labels,
        'months_clinical':   months_clinical,
        'months_autopsy':    months_autopsy,
        'type_data':         list(type_data),
        'death_data':        list(death_data),
        'page_title':        'Dashboard',
        'active_nav':        'dashboard',
    }
    return render(request, 'dashboard/index.html', context)
