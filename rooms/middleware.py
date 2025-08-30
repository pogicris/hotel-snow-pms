from .models import ActivityLog

class ActivityLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if not request.path.startswith('/admin') and not request.path.startswith('/static'):
            user = request.user if request.user.is_authenticated else None
            
            action = f"Viewed {request.path}"
            if request.method == 'POST':
                action = f"Made a POST request to {request.path}"

            ActivityLog.objects.create(
                user=user,
                action=action,
                ip_address=request.META.get('REMOTE_ADDR'),
                path=request.path,
                method=request.method
            )

        return response
