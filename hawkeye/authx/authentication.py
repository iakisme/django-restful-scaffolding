from rest_framework_jwt.authentication import BaseJSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication
from django.conf import settings

class JSONWebTokenAuthenticationQS(BaseJSONWebTokenAuthentication):
    def get_jwt_value(self, request):
        return request.query_params.get(settings.QS_JWT_KEY)

class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return
