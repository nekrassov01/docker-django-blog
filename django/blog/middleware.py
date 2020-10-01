from django.conf import settings
from django.urls import reverse 
from django.core.exceptions import PermissionDenied

""" 許可IP以外からの管理サイトへのアクセスを禁止する """
class IpRestrictMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        allowed_ips = settings.ALLOWED_IPS
        ip = request.META.get('REMOTE_ADDR')
        admin_index = reverse('admin:index')
        if request.path.startswith(admin_index):
            if ip not in allowed_ips:
                raise PermissionDenied
        response = self.get_response(request)
        return response