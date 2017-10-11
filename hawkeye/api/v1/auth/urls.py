from django.conf.urls import url, include
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register('users', views.UserViewSet)
router.register('permissions', views.PermissionViewSet)
router.register('userobjectpermissions', views.UserObjectPermissionViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^token/$', views.obtain_jwt_token),
    url(r'^token/refresh/$', views.refresh_jwt_token),
    url(r'^token/verify/$', views.verify_jwt_token),
    url(r'^register/$', views.register),
    url(r'^login/$', views.login),
    url(r'^grant_license/$', views.grantYunquAuthorization),
    url(r'^license_info/$', views.license_info),
    url(r'^test/$', views.test),
]
