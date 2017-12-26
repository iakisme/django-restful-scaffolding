from django.conf.urls import url, include
from rest_framework_bulk.routes import BulkRouter

from api.v1.monitor import views
from api.v1.monitor.views import DreamViewSet

router = BulkRouter()
router.register('dream', DreamViewSet)

urlpatterns = (
    url(r'^', include(router.urls)),
    url(r'^send_code/$', views.send_code),
    # url(r'^validate_code/$', views.validate_code),
    url(r'^upload_file/$', views.upload_file),
    url(r'^upload_image/$', views.upload_image),
    url(r'^export_file/$', views.export_file),
)
