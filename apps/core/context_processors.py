from apps.cases.models   import ForensicCase
from apps.patients.models import Patient
from apps.evidence.models import Evidence
from apps.reports.models  import CourtReport


def nav_counts(request):
    """Inject sidebar badge counts into every template context."""
    if not request.user.is_authenticated:
        return {}
    try:
        return {
            'nav_active_cases':    ForensicCase.objects.exclude(case_status__in=['Closed', 'Archived']).count(),
            'nav_pending_reports': CourtReport.objects.filter(report_status__in=['Draft', 'Generated', 'Reviewed']).count(),
            'nav_total_patients':  Patient.objects.count(),
            'nav_pending_evidence': Evidence.objects.filter(analysis_status='Pending').count(),
        }
    except Exception:
        return {}
