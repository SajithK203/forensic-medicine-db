from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta, datetime
import calendar

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
    critical_cases   = ForensicCase.objects.filter(priority='Critical').exclude(case_status__in=['Closed', 'Archived']).count()
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
        
        # SQLite has a bug with __month/__year lookups when USE_TZ=True.
        # We use __range to get accurate counts.
        _, last_day = calendar.monthrange(dt.year, dt.month)
        start_date = timezone.make_aware(datetime(dt.year, dt.month, 1))
        end_date   = timezone.make_aware(datetime(dt.year, dt.month, last_day, 23, 59, 59))

        months_clinical.append(
            ForensicCase.objects.filter(
                incident_date__range=(start_date, end_date),
                case_type__in=['Clinical Forensic', 'Clinical & Autopsy']
            ).count()
        )
        months_autopsy.append(
            ForensicCase.objects.filter(
                incident_date__range=(start_date, end_date),
                case_type__in=['Autopsy', 'Clinical & Autopsy']
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

    # ── Role-specific context extensions ──────────────────────────────────────
    user = request.user
    my_assigned_cases = []
    my_pending_autopsies_count = 0
    my_pending_reports_count = 0
    lab_pending_tests_count = 0
    lab_evidence_queue = []
    locked_users_count = 0

    if getattr(user, 'is_doctor', False):
        my_assigned_cases = (
            ForensicCase.objects
            .filter(doctor__staff__email=user.email)
            .exclude(case_status__in=['Closed', 'Archived'])
            .select_related('patient', 'doctor')
            .order_by('-incident_date')[:5]
        )
        my_pending_autopsies_count = Postmortem.objects.filter(doctor__staff__email=user.email, report_status='Pending').count()
        my_pending_reports_count = CourtReport.objects.filter(doctor__staff__email=user.email, report_status__in=['Draft', 'Generated']).count()

    elif getattr(user, 'is_lab_tech', False):
        lab_pending_tests_count = Evidence.objects.filter(analysis_status='Pending').count()
        lab_evidence_queue = Evidence.objects.filter(analysis_status='Pending').select_related('case').order_by('-collection_date')[:5]

    elif getattr(user, 'is_administrator', False):
        from apps.accounts.models import CustomUser
        locked_users_count = CustomUser.objects.filter(is_locked=True).count()

    if request.GET.get('ajax') == '1':
        return JsonResponse({
            'kpis': {
                'total_cases': total_cases,
                'active_cases': active_cases,
                'critical_cases': critical_cases,
                'total_patients': total_patients,
                'pending_evidence': pending_evidence,
                'pending_reports': pending_reports,
            },
            'charts': {
                'trend': {
                    'labels': months_labels,
                    'clinical': months_clinical,
                    'autopsy': months_autopsy
                },
                'type': {
                    'labels': [d['case_type'] for d in type_data],
                    'data': [d['count'] for d in type_data]
                },
                'death': {
                    'labels': [d['death_type'] or 'Unknown' for d in death_data],
                    'data': [d['count'] for d in death_data]
                }
            }
        })

    context = {
        'total_cases':                total_cases,
        'active_cases':               active_cases,
        'critical_cases':             critical_cases,
        'total_patients':             total_patients,
        'pending_reports':            pending_reports,
        'pending_evidence':           pending_evidence,
        'recent_cases':               recent_cases,
        'overdue_cases':              overdue_cases,
        'recent_logs':                recent_logs,
        'my_assigned_cases':          my_assigned_cases,
        'my_pending_autopsies_count': my_pending_autopsies_count,
        'my_pending_reports_count':   my_pending_reports_count,
        'lab_pending_tests_count':    lab_pending_tests_count,
        'lab_evidence_queue':         lab_evidence_queue,
        'locked_users_count':         locked_users_count,
        # Chart data (as Python lists — serialised in template)
        'months_labels':              months_labels,
        'months_clinical':            months_clinical,
        'months_autopsy':             months_autopsy,
        'type_data':                  list(type_data),
        'death_data':                 list(death_data),
        'page_title':                 'Dashboard',
        'active_nav':                 'dashboard',
    }
    return render(request, 'dashboard/index.html', context)


@login_required
def global_search(request):
    """Global navbar search — queries Patients, Cases, Evidence and Reports."""
    from apps.evidence.models import Evidence
    from apps.reports.models  import CourtReport

    q = request.GET.get('q', '').strip()
    patients  = []
    cases     = []
    evidence  = []
    reports   = []

    if q:
        patients = Patient.objects.filter(
            Q(patient_id__icontains=q) |
            Q(full_name__icontains=q) |
            Q(nic_passport__icontains=q) |
            Q(contact_no__icontains=q) |
            Q(district__icontains=q)
        ).order_by('full_name')[:20]

        cases = ForensicCase.objects.select_related('patient', 'doctor').filter(
            Q(case_id__icontains=q) |
            Q(case_number__icontains=q) |
            Q(patient__full_name__icontains=q) |
            Q(incident_type__icontains=q) |
            Q(incident_location__icontains=q) |
            Q(police_report_no__icontains=q) |
            Q(court_case_no__icontains=q) |
            Q(case_status__icontains=q) |
            Q(case_type__icontains=q)
        ).order_by('-created_at')[:20]

        evidence = Evidence.objects.select_related('case').filter(
            Q(evidence_id__icontains=q) |
            Q(evidence_type__icontains=q) |
            Q(evidence_description__icontains=q) |
            Q(barcode_number__icontains=q) |
            Q(case__case_number__icontains=q)
        ).order_by('-collection_date')[:10]

        reports = CourtReport.objects.select_related('case').filter(
            Q(report_id__icontains=q) |
            Q(court_name__icontains=q) |
            Q(report_title__icontains=q) |
            Q(case__case_number__icontains=q) |
            Q(report_status__icontains=q)
        ).order_by('-created_at')[:10]

    # Evaluate QuerySets into lists (single DB hit each, safe for sliced QS)
    patients = list(patients)
    cases    = list(cases)
    evidence = list(evidence)
    reports  = list(reports)

    total_results = len(patients) + len(cases) + len(evidence) + len(reports)

    return render(request, 'core/search_results.html', {
        'q':             q,
        'patients':      patients,
        'cases':         cases,
        'evidence':      evidence,
        'reports':       reports,
        'total_results': total_results,
        'page_title':    f'Search: {q}' if q else 'Search',
        'active_nav':    '',
    })

