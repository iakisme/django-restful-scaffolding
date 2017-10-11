from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin
from .yunquAuthorizationUtil import get_lisence_info

class YunquAuthorizationCheckMiddleware(MiddlewareMixin):
    """
    Middleware that handles whether license validates
    """


    def process_request(self, request):
        login_url = '/api/v1/auth/login/'
        license_info_url = ['/api/v1/auth/license_info/','/api/v1/auth/grant_license/']
        if request.path_info in login_url or request.path_info in license_info_url:
            return

        #return redirect('http://localhost:3000/login/')
        info = get_lisence_info()
        if not info.get('certificated', False) \
            or (info.get('days') is not None and info['days']<=0):
            #return redirect('http://localhost:3000/login/')
            return redirect('http://localhost:3000/activation/')
        return





