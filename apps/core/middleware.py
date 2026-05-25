from apps.core.models import ActivityLog


class ActivityLogMiddleware:
    """Logs every authenticated page view to the ActivityLog table."""

    SKIP_PATHS = ['/static/', '/media/', '/favicon.ico']

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.__call_inner(request)
        return response

    def __call_inner(self, request):
        response = self.get_response(request)

        if (request.user.is_authenticated
                and request.method == 'GET'
                and not any(request.path.startswith(p) for p in self.SKIP_PATHS)):
            try:
                ActivityLog.objects.create(
                    user          = request.user,
                    username      = request.user.username,
                    action_type   = 'VIEW',
                    model_name    = '',
                    record_id     = '',
                    action_details = f'GET {request.path}',
                    ip_address    = self._get_ip(request),
                    user_agent    = request.META.get('HTTP_USER_AGENT', '')[:500],
                )
            except Exception:
                pass  # Never let logging break the request

        return response

    @staticmethod
    def _get_ip(request):
        forwarded = request.META.get('HTTP_X_FORWARDED_FOR')
        if forwarded:
            return forwarded.split(',')[0].strip()
        return request.META.get('REMOTE_ADDR')


def log_action(user, action_type, model_name='', record_id='', details='', request=None):
    """Helper function to log a write action from views."""
    ip = None
    ua = ''
    if request:
        forwarded = request.META.get('HTTP_X_FORWARDED_FOR')
        ip = forwarded.split(',')[0].strip() if forwarded else request.META.get('REMOTE_ADDR')
        ua = request.META.get('HTTP_USER_AGENT', '')[:500]
    try:
        ActivityLog.objects.create(
            user           = user,
            username       = user.username,
            action_type    = action_type,
            model_name     = model_name,
            record_id      = str(record_id),
            action_details = details,
            ip_address     = ip,
            user_agent     = ua,
        )
    except Exception:
        pass
